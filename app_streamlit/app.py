from __future__ import annotations

import io
import base64
import warnings
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import rasterio
import folium
from PIL import Image
from rasterio.io import MemoryFile
from rasterio.warp import transform_bounds
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Klasifikasi Tutupan Lahan Sentinel-2",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = __import__("pathlib").Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "random_forest_model.pkl"

# Harus identik dengan notebook training:
# FITUR_COLS = ['B03', 'B04', 'B08', 'B11', 'NDVI', 'NDWI', 'NDBI']
CLASS_INFO = {
    "built_up":   {"label": "Lahan Terbangun", "color": "#e41a1c"},
    "farmland":   {"label": "Lahan Pertanian", "color": "#e6ab02"},
    "water_body": {"label": "Badan Air", "color": "#1f78b4"},
    "forest":     {"label": "Hutan", "color": "#228b22"},
    "mangrove":   {"label": "Hutan Mangrove", "color": "#00a884"},
}

st.title("🛰️ Klasifikasi Tutupan Lahan Sentinel-2")
st.write(
    "Unggah citra Sentinel-2 GeoTIFF, jalankan model Random Forest tersimpan, "
    "lalu lihat peta interaktif dan statistik hasil klasifikasi."
)

def normalized_difference(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Formula sama dengan notebook: (a-b)/(a+b), nol jika penyebut nol."""
    denominator = a + b
    result = np.zeros(a.shape, dtype=np.float32)
    np.divide(a - b, denominator, out=result, where=denominator != 0)
    return result

def extract_features(src):
    # File openEO.tif yang diberikan memiliki 4 band, deskripsi B03/B04/B08/B11.
    if src.count != 4:
        raise ValueError(
            f"Raster ini memiliki {src.count} band, sedangkan notebook melatih model "
            "dengan 4 band: B03, B04, B08, B11."
        )

    descriptions = [str(x).upper() if x else "" for x in src.descriptions]
    expected = ["B03", "B04", "B08", "B11"]
    if all(descriptions) and descriptions != expected:
        raise ValueError(
            f"Urutan band terdeteksi {descriptions}, tetapi aplikasi mengharapkan {expected}. "
            "Band harus sesuai urutan yang dipakai saat ekstraksi fitur training."
        )

    # PENTING: notebook training memakai nilai raster asli (DN), tidak dibagi 10.000.
    # Hanya indeks rasio yang dihitung dari nilai tersebut.
    b03, b04, b08, b11 = [
        src.read(i).astype(np.float32) for i in range(1, 5)
    ]

    ndvi = normalized_difference(b08, b04)
    ndwi = normalized_difference(b03, b08)
    ndbi = normalized_difference(b11, b08)

    # Urutan wajib sesuai FITUR_COLS pada notebook dan model PKL.
    features = np.stack(
        [b03, b04, b08, b11, ndvi, ndwi, ndbi],
        axis=-1,
    ).astype(np.float32)

    valid = np.all(np.isfinite(features), axis=-1)
    if src.nodata is not None:
        valid &= src.read_masks(1) > 0
        valid &= b03 != src.nodata
    # File sumber memakai -32768 untuk NoData.
    valid &= b03 != -32768
    valid &= b04 != -32768
    valid &= b08 != -32768
    valid &= b11 != -32768

    return features, valid

def predict_raster(uploaded_bytes: bytes, model):
    with MemoryFile(uploaded_bytes) as memfile:
        with memfile.open() as src:
            features, valid = extract_features(src)
            if not np.any(valid):
                raise ValueError("Tidak ada piksel valid setelah penyaringan NoData.")

            expected_n = getattr(model, "n_features_in_", None)
            if expected_n != features.shape[-1]:
                raise ValueError(
                    f"Model mengharapkan {expected_n} fitur, tetapi aplikasi menyiapkan "
                    f"{features.shape[-1]}. Periksa ulang model dan urutan fitur."
                )

            model_features = getattr(model, "feature_names_in_", None)
            if model_features is not None:
                wanted = ["B03", "B04", "B08", "B11", "NDVI", "NDWI", "NDBI"]
                if list(model_features) != wanted:
                    raise ValueError(
                        f"Nama/urutan fitur pada model tidak cocok: {list(model_features)}"
                    )

            flat = features[valid]
            pred_parts = []
            progress = st.progress(0, text="Menjalankan Random Forest...")
            batch_size = 100_000
            for start in range(0, len(flat), batch_size):
                end = min(start + batch_size, len(flat))
                batch = flat[start:end]
                # Jika model dilatih dengan DataFrame, gunakan nama kolom yang sama
                # untuk menghindari warning dan menjaga urutan fitur.
                feature_names = getattr(model, "feature_names_in_", None)
                if feature_names is not None:
                    batch_input = pd.DataFrame(batch, columns=list(feature_names))
                else:
                    batch_input = batch
                pred_parts.append(model.predict(batch_input))
                progress.progress(
                    end / len(flat),
                    text=f"Memproses {end:,} dari {len(flat):,} piksel",
                )
            progress.empty()

            predicted = np.concatenate(pred_parts)
            labels = [str(x) for x in model.classes_]
            label_to_code = {label: idx + 1 for idx, label in enumerate(labels)}
            code_to_label = {code: label for label, code in label_to_code.items()}

            classified = np.zeros((src.height, src.width), dtype=np.uint8)
            classified[valid] = np.array(
                [label_to_code[str(x)] for x in predicted],
                dtype=np.uint8,
            )

            return {
                "classified": classified,
                "valid": valid,
                "transform": src.transform,
                "crs": src.crs,
                "profile": src.profile.copy(),
                "height": src.height,
                "width": src.width,
                "code_to_label": code_to_label,
                "model_classes": labels,
            }

def style_for(label, code):
    info = CLASS_INFO.get(label)
    if info:
        return info["label"], info["color"]
    palette = ["#e41a1c", "#e6ab02", "#1f78b4", "#228b22", "#00a884"]
    return label, palette[(code - 1) % len(palette)]

def make_stats(classified, valid, transform, code_to_label):
    codes, counts = np.unique(classified[valid], return_counts=True)
    pixel_area_km2 = abs(transform.a * transform.e) / 1_000_000
    total = int(counts.sum())
    rows = []
    for code, count in zip(codes, counts):
        label = code_to_label[int(code)]
        display, _ = style_for(label, int(code))
        rows.append({
            "Kode": int(code),
            "Kelas": display,
            "Label model": label,
            "Jumlah piksel": int(count),
            "Luas (km²)": round(int(count) * pixel_area_km2, 4),
            "Persentase (%)": round(int(count) / total * 100, 2),
        })
    return pd.DataFrame(rows), total

def make_class_overlays(classified, valid, transform, crs, code_to_label, max_size=1400):
    """Buat PNG transparan terpisah untuk tiap kelas agar kelas bisa dinyalakan/dimatikan."""
    h, w = classified.shape
    step = max(1, int(np.ceil(max(h, w) / max_size)))
    small = classified[::step, ::step]
    small_valid = valid[::step, ::step]

    present = sorted(int(v) for v in np.unique(small[small_valid]))
    west, south, east, north = rasterio.transform.array_bounds(h, w, transform)
    if crs is None:
        raise ValueError("Raster tidak memiliki CRS, sehingga tidak bisa ditempatkan di peta.")
    west, south, east, north = transform_bounds(
        crs, "EPSG:4326", west, south, east, north, densify_pts=21
    )
    bounds = [[south, west], [north, east]]

    overlays = {}
    for code in present:
        label = code_to_label[code]
        display, color = style_for(label, code)
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        rgba = np.zeros((small.shape[0], small.shape[1], 4), dtype=np.uint8)
        mask = (small == code) & small_valid
        rgba[mask, 0] = rgb[0]
        rgba[mask, 1] = rgb[1]
        rgba[mask, 2] = rgb[2]
        rgba[mask, 3] = 205

        buf = io.BytesIO()
        Image.fromarray(rgba, mode="RGBA").save(buf, format="PNG", optimize=True)
        overlays[code] = {
            "png": buf.getvalue(),
            "display": display,
            "color": color,
            "label": label,
        }
    return overlays, bounds, present

def build_interactive_map(overlays, bounds, present_codes, code_to_label):
    center = [
        (bounds[0][0] + bounds[1][0]) / 2,
        (bounds[0][1] + bounds[1][1]) / 2,
    ]
    fmap = folium.Map(location=center, zoom_start=11, tiles=None, control_scale=True)
    folium.TileLayer("OpenStreetMap", name="Peta jalan", control=True).add_to(fmap)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Tiles © Esri",
        name="Citra satelit",
        control=True,
    ).add_to(fmap)

    # Satu overlay per kelas. Layer Control dapat mengaktifkan/nonaktifkan tiap kelas.
    for code in present_codes:
        item = overlays[code]
        png_data_uri = "data:image/png;base64," + base64.b64encode(item["png"]).decode("ascii")
        folium.raster_layers.ImageOverlay(
            image=png_data_uri,
            bounds=bounds,
            opacity=1,
            name=item["display"],
            overlay=True,
            control=True,
            show=True,
            interactive=True,
            cross_origin=False,
            zindex=10 + code,
        ).add_to(fmap)

    folium.LayerControl(collapsed=False).add_to(fmap)
    fmap.fit_bounds(bounds)
    return fmap

uploaded = st.file_uploader(
    "1. Unggah citra Sentinel-2 (.tif)",
    type=["tif", "tiff"],
    help="Gunakan openEO.tif dengan empat band: B03, B04, B08, B11. Jangan gunakan hasil_klasifikasi_rf.tif.",
)

if uploaded:
    st.caption(f"File: {uploaded.name} · {uploaded.size / (1024 * 1024):.2f} MB")
    if st.button("2. Proses model dan tampilkan peta", type="primary", use_container_width=True):
        try:
            if not MODEL_PATH.exists():
                st.error(f"File model tidak ditemukan: {MODEL_PATH}")
                st.stop()

            # Peringatan versi sklearn tidak selalu menggagalkan prediksi, tetapi perlu disamakan
            # dengan versi saat model dibuat untuk demo yang reproducible.
            # Satu model berisi banyak estimator pohon; versi sklearn yang berbeda bisa
            # memunculkan peringatan berulang untuk setiap pohon. Tahan saat load dan tampilkan
            # maksimal satu pesan informatif, agar layar demo tidak dipenuhi pesan identik.
            version_mismatch = False
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                model = joblib.load(MODEL_PATH)
            version_mismatch = any(
                "InconsistentVersionWarning" in warning.category.__name__
                for warning in caught
            )
            if version_mismatch:
                st.info(
                    "Model dibuat dengan versi scikit-learn berbeda. Prediksi berhasil dijalankan, "
                    "tetapi untuk hasil demo yang reproducible samakan versi pustaka dengan versi training."
                )

            result = predict_raster(uploaded.getvalue(), model)
            classified = result["classified"]
            valid = result["valid"]
            code_to_label = result["code_to_label"]
            stats, total = make_stats(classified, valid, result["transform"], code_to_label)

            st.success("Klasifikasi selesai.")
            st.write("**Kelas yang dikenal model:** " + ", ".join(result["model_classes"]))
            if len(result["model_classes"]) != 5:
                st.warning("Model tidak memiliki lima kelas. Periksa dataset dan model PKL sebelum demo.")

            c1, c2, c3 = st.columns(3)
            c1.metric("Piksel valid", f"{total:,}")
            c2.metric("Kelas terprediksi", str(len(stats)))
            c3.metric("Ukuran raster", f"{result['width']:,} × {result['height']:,}")

            st.subheader("3. Peta klasifikasi interaktif")
            overlays, bounds, present_codes = make_class_overlays(
                classified, valid, result["transform"], result["crs"], code_to_label
            )
            fmap = build_interactive_map(overlays, bounds, present_codes, code_to_label)
            st_folium(
                fmap,
                use_container_width=True,
                height=650,
                returned_objects=[],
                key="rf_interactive_map",
            )
            st.caption("Gunakan Layer Control di kanan atas peta untuk menyalakan/mematikan tiap kelas secara terpisah, serta memilih peta jalan atau citra satelit.")

            st.subheader("4. Statistik tutupan lahan")
            st.dataframe(stats, use_container_width=True, hide_index=True)

            out_profile = result["profile"].copy()
            out_profile.update(driver="GTiff", count=1, dtype="uint8", nodata=0, compress="lzw")
            tif_bytes = io.BytesIO()
            with MemoryFile() as mem:
                with mem.open(**out_profile) as dst:
                    dst.write(classified, 1)
                tif_bytes.write(mem.read())

            st.download_button(
                "Unduh hasil klasifikasi GeoTIFF",
                data=tif_bytes.getvalue(),
                file_name="hasil_klasifikasi_rf.tif",
                mime="image/tiff",
            )
            st.download_button(
                "Unduh statistik CSV",
                data=stats.to_csv(index=False).encode("utf-8-sig"),
                file_name="statistik_tutupan_lahan.csv",
                mime="text/csv",
            )
            st.caption("Kode kelas pada GeoTIFF mengikuti urutan classes_ model. CSV menyimpan pasangan kode dan nama kelas.")
        except Exception as exc:
            st.error(f"Gagal memproses raster: {exc}")
            st.exception(exc)
else:
    st.info(
        "Alur demo: unggah openEO.tif → ekstraksi 7 fitur sesuai notebook → prediksi model PKL "
        "→ peta interaktif → statistik dan unduhan."
    )
