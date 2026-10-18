
from pathlib import Path
import io
import base64

import numpy as np
import pandas as pd
import rasterio
import streamlit as st
import folium

from PIL import Image
from rasterio.enums import Resampling
from rasterio.warp import transform_bounds
from rasterio.transform import array_bounds
from streamlit_folium import st_folium


# ============================================================
# 1. KONFIGURASI APLIKASI
# ============================================================
st.set_page_config(
    page_title="Klasifikasi Tutupan Lahan Jawa Timur",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
RASTER_PATH = BASE_DIR / "hasil_klasifikasi_jawa_timur_rf.tif"

NODATA_CODE = 0
MAX_MAP_SIZE = 1400
BLOCK_ROWS = 512

CLASS_INFO = {
    1: {"name": "built_up", "label": "Lahan Terbangun", "color": "#e41a1c"},
    2: {"name": "farmland", "label": "Lahan Pertanian", "color": "#e6ab02"},
    3: {"name": "water_body", "label": "Badan Air", "color": "#1f78b4"},
    4: {"name": "forest", "label": "Hutan", "color": "#228b22"},
    5: {"name": "mangrove", "label": "Hutan Mangrove", "color": "#00a884"},
}


# ============================================================
# 2. HEADER DAN VALIDASI FILE
# ============================================================
st.title("🛰️ Klasifikasi Tutupan Lahan Jawa Timur")
st.markdown(
    """
    Peta tutupan lahan hasil klasifikasi **Random Forest**
    menggunakan citra Sentinel-2. Hasil klasifikasi telah
    diproses sebelumnya dan ditampilkan langsung tanpa
    unggah citra atau prediksi ulang.
    """
)

if not RASTER_PATH.exists():
    st.error(f"Raster hasil klasifikasi tidak ditemukan: {RASTER_PATH}")
    st.info(
        "Letakkan hasil_klasifikasi_jawa_timur_rf.tif "
        "di folder yang sama dengan app.py."
    )
    st.stop()


# ============================================================
# 3. STATISTIK RASTER, DIBACA PER BLOK
# ============================================================
@st.cache_data(show_spinner="Membaca statistik raster...")
def calculate_statistics(raster_path, block_rows=512):
    counts = {code: 0 for code in CLASS_INFO}
    total_pixels = 0
    nodata_pixels = 0

    with rasterio.open(raster_path) as src:
        height, width = src.height, src.width
        transform = src.transform
        crs = src.crs
        file_size = Path(raster_path).stat().st_size

        for row in range(0, height, block_rows):
            rows = min(block_rows, height - row)
            window = rasterio.windows.Window(0, row, width, rows)
            arr = src.read(1, window=window)

            valid = (arr >= 1) & (arr <= 5)
            total_pixels += int(valid.sum())
            nodata_pixels += int((~valid).sum())

            values, amounts = np.unique(arr[valid], return_counts=True)
            for value, amount in zip(values, amounts):
                counts[int(value)] += int(amount)

    pixel_area_km2 = abs(transform.a * transform.e) / 1_000_000
    rows = []

    for code, info in CLASS_INFO.items():
        count = counts[code]
        rows.append({
            "Kode": code,
            "Kelas": info["label"],
            "Label": info["name"],
            "Jumlah Piksel": count,
            "Luas (km²)": round(count * pixel_area_km2, 2),
            "Proporsi (%)": round(
                count / total_pixels * 100, 2
            ) if total_pixels else 0,
        })

    return {
        "stats": pd.DataFrame(rows),
        "counts": counts,
        "total": total_pixels,
        "nodata": nodata_pixels,
        "width": width,
        "height": height,
        "crs": str(crs),
        "transform": transform,
        "file_size": file_size,
    }


# ============================================================
# 4. RASTER RESOLUSI RENDAH UNTUK VISUALISASI
# ============================================================
@st.cache_data(show_spinner="Menyiapkan peta...")
def prepare_map_raster(raster_path, max_size=1400):
    with rasterio.open(raster_path) as src:
        height, width = src.height, src.width

        scale = min(1, max_size / max(height, width))
        out_height = max(1, int(height * scale))
        out_width = max(1, int(width * scale))

        # Membaca versi kecil untuk peta, bukan seluruh raster.
        small = src.read(
            1,
            out_shape=(out_height, out_width),
            resampling=Resampling.nearest,
        )

        west, south, east, north = array_bounds(
            height, width, src.transform
        )

        if src.crs is None:
            raise ValueError("Raster tidak memiliki CRS.")

        west, south, east, north = transform_bounds(
            src.crs,
            "EPSG:4326",
            west, south, east, north,
            densify_pts=21,
        )

    bounds = [[south, west], [north, east]]
    overlays = {}

    for code, info in CLASS_INFO.items():
        mask = small == code
        if not mask.any():
            continue

        rgb_hex = info["color"].lstrip("#")
        rgb = tuple(
            int(rgb_hex[i:i + 2], 16)
            for i in (0, 2, 4)
        )

        rgba = np.zeros(
            (out_height, out_width, 4),
            dtype=np.uint8,
        )
        rgba[mask, :3] = rgb
        rgba[mask, 3] = 205

        buffer = io.BytesIO()
        Image.fromarray(rgba).save(
            buffer, format="PNG", optimize=True
        )
        png_uri = (
            "data:image/png;base64,"
            + base64.b64encode(buffer.getvalue()).decode("ascii")
        )

        overlays[code] = {
            "uri": png_uri,
            "label": info["label"],
            "name": info["name"],
            "color": info["color"],
        }

    return overlays, bounds, out_width, out_height


# ============================================================
# 5. MEMBANGUN PETA FOLIUM
# ============================================================
def build_map(overlays, bounds):
    center = [
        (bounds[0][0] + bounds[1][0]) / 2,
        (bounds[0][1] + bounds[1][1]) / 2,
    ]

    fmap = folium.Map(
        location=center,
        zoom_start=7,
        tiles=None,
        control_scale=True,
    )

    folium.TileLayer(
        tiles="OpenStreetMap",
        name="Peta Jalan",
        control=True,
    ).add_to(fmap)

    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Tiles © Esri",
        name="Citra Satelit",
        control=True,
    ).add_to(fmap)

    for code, item in overlays.items():
        folium.raster_layers.ImageOverlay(
            image=item["uri"],
            bounds=bounds,
            opacity=0.85,
            name=f'{code} - {item["label"]}',
            overlay=True,
            control=True,
            show=True,
            interactive=True,
        ).add_to(fmap)

    legend_items = "".join(
        f"""
        <div style="margin:5px 0;">
            <span style="
                display:inline-block;width:14px;height:14px;
                background:{item['color']};margin-right:7px;
                border-radius:3px;"></span>
            <b>{item['name']}</b> ({item['label']})
        </div>
        """
        for item in overlays.values()
    )

    legend_html = f"""
    <div style="
        position:fixed;bottom:25px;left:25px;z-index:9999;
        background:rgba(255,255,255,0.95);
        border:1px solid #777;border-radius:8px;
        padding:12px 15px;font-family:Arial,sans-serif;
        font-size:12px;box-shadow:0 2px 8px #777;">
        <b style="font-size:14px;">Legenda Tutupan Lahan</b>
        <hr style="margin:7px 0;">
        {legend_items}
        <div style="margin-top:6px;color:#666;">
            Transparan = NoData
        </div>
    </div>
    """

    fmap.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl(collapsed=False).add_to(fmap)
    fmap.fit_bounds(bounds)

    return fmap


# ============================================================
# 6. TAMPILKAN DASHBOARD SECARA OTOMATIS
# ============================================================
try:
    info = calculate_statistics(str(RASTER_PATH), BLOCK_ROWS)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Piksel Valid", f"{info['total']:,}")
    col2.metric("Jumlah Kelas", "5")
    col3.metric(
        "Resolusi Raster",
        f"{info['width']:,} × {info['height']:,}",
    )
    col4.metric(
        "Ukuran File",
        f"{info['file_size'] / (1024**2):,.2f} MB",
    )

    st.caption(
        f"CRS: {info['crs']} | "
        f"Piksel NoData: {info['nodata']:,}"
    )

    st.subheader("Peta Interaktif Tutupan Lahan")
    overlays, bounds, map_width, map_height = prepare_map_raster(
        str(RASTER_PATH), MAX_MAP_SIZE
    )

    fmap = build_map(overlays, bounds)

    st_folium(
        fmap,
        use_container_width=True,
        height=650,
        returned_objects=[],
        key="peta_tutupan_lahan_jawa_timur",
    )

    st.caption(
        f"Resolusi tampilan peta: {map_width:,} × {map_height:,} piksel. "
        "Gunakan kontrol layer di kanan atas untuk memilih kelas "
        "atau mengganti basemap."
    )

    st.subheader("Statistik Tutupan Lahan")
    st.dataframe(
        info["stats"],
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Distribusi Luas Tutupan Lahan")
    chart_data = info["stats"].set_index("Kelas")["Luas (km²)"]
    st.bar_chart(chart_data)

    csv_bytes = info["stats"].to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        "Unduh Statistik CSV",
        data=csv_bytes,
        file_name="statistik_tutupan_lahan_jawa_timur.csv",
        mime="text/csv",
    )

except Exception as exc:
    st.error(f"Gagal menampilkan hasil klasifikasi: {exc}")
    st.exception(exc)
