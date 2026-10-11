# Klasifikasi Tutupan Lahan Menggunakan Citra Sentinel-2 di Provinsi Jawa Timur

## 1. Business Understanding

### 1.1 Latar Belakang

Informasi mengenai tutupan lahan memiliki peran penting dalam pemantauan kondisi lingkungan, pengelolaan sumber daya alam, dan perencanaan wilayah. Perbedaan karakteristik tutupan lahan, seperti kawasan terbangun, lahan pertanian, badan air, hutan non-mangrove, dan mangrove, memerlukan pendekatan klasifikasi yang mampu mengenali karakteristik masing-masing kelas.

Citra satelit Sentinel-2 menyediakan informasi spektral yang dapat dimanfaatkan untuk membedakan tutupan lahan berdasarkan karakteristik reflektansi permukaan. Kombinasi kanal spektral yang sesuai dapat digunakan untuk mengidentifikasi perbedaan antara vegetasi, kawasan terbangun, dan badan air, termasuk mendukung pembedaan mangrove dengan hutan non-mangrove.

Penelitian ini memanfaatkan citra Sentinel-2 Level-2A dari Copernicus Data Space Ecosystem sebagai sumber data utama. Data referensi tutupan lahan diperoleh melalui digitasi poligon secara manual pada wilayah Muncar, Teluk Pangpang, Tegaldlimo, dan sekitarnya di Kabupaten Banyuwangi, Jawa Timur. Poligon tersebut digunakan sebagai data referensi untuk membangun dan mengevaluasi model klasifikasi tutupan lahan.

Penelitian difokuskan pada lima kelas tutupan lahan, yaitu kawasan terbangun (*built-up*), lahan pertanian (*farmland*), badan air (*water body*), hutan non-mangrove (*forest*), dan mangrove. Model yang dikembangkan selanjutnya direncanakan untuk diterapkan pada wilayah Provinsi Jawa Timur dan hasilnya disajikan melalui aplikasi berbasis web menggunakan Streamlit.

### 1.2 Identifikasi Masalah

Permasalahan yang menjadi dasar penelitian ini adalah sebagai berikut.

1. Karakteristik spektral antarjenis tutupan lahan dapat memiliki kemiripan sehingga diperlukan kombinasi fitur yang sesuai untuk mendukung proses klasifikasi.
2. Pembedaan antara mangrove dan hutan non-mangrove memerlukan data referensi yang tepat serta evaluasi hasil klasifikasi yang memadai.
3. Data referensi hasil digitasi perlu diolah menjadi dataset yang sesuai untuk pelatihan dan pengujian model klasifikasi.
4. Hasil klasifikasi perlu disajikan dalam bentuk peta interaktif agar distribusi spasial setiap kelas tutupan lahan dapat diamati dengan lebih mudah.
5. Penerapan model dari wilayah sampel di Kabupaten Banyuwangi ke wilayah Provinsi Jawa Timur perlu memperhatikan keterbatasan keterwakilan sampel dan kemampuan generalisasi model.

### 1.3 Tujuan Penelitian

Penelitian ini bertujuan untuk:

1. Memanfaatkan citra Sentinel-2 Level-2A untuk memperoleh informasi spektral yang mendukung klasifikasi tutupan lahan.
2. Membangun model klasifikasi untuk membedakan lima kelas tutupan lahan, yaitu kawasan terbangun, lahan pertanian, badan air, hutan non-mangrove, dan mangrove.
3. Mengevaluasi kinerja model menggunakan metrik evaluasi klasifikasi yang sesuai, meliputi *confusion matrix*, akurasi, dan Cohen's Kappa, serta metrik per kelas.
4. Menghasilkan peta klasifikasi tutupan lahan yang dapat divisualisasikan secara interaktif melalui aplikasi Streamlit.
5. Mengembangkan implementasi awal klasifikasi tutupan lahan untuk wilayah Provinsi Jawa Timur dengan memperhatikan keterbatasan data referensi dan validasi spasial.

### 1.4 Business Objective

Tujuan implementasi dari penelitian ini adalah menyediakan prototipe aplikasi pemetaan tutupan lahan yang mampu menampilkan hasil klasifikasi secara interaktif. Aplikasi dirancang untuk menampilkan peta dasar, lapisan hasil klasifikasi, pilihan kelas yang ingin ditampilkan, serta ringkasan luas dan persentase setiap kelas.

Aplikasi juga direncanakan menampilkan informasi evaluasi model agar pengguna dapat memahami kinerja klasifikasi yang digunakan. Estimasi luas tutupan lahan akan dihitung berdasarkan hasil klasifikasi raster dan resolusi spasial yang digunakan.

### 1.5 Manfaat Penelitian

Penelitian ini diharapkan memberikan manfaat sebagai berikut.

1. **Manfaat akademis:** menjadi contoh penerapan penginderaan jauh dan klasifikasi berbasis data spektral Sentinel-2 untuk pemetaan tutupan lahan.
2. **Manfaat teknis:** menghasilkan alur pengolahan data yang mencakup persiapan data referensi, ekstraksi fitur, pelatihan model, evaluasi, dan visualisasi hasil.
3. **Manfaat praktis:** menyediakan prototipe peta interaktif yang memudahkan pengamatan distribusi lima kelas tutupan lahan.
4. **Manfaat pengembangan:** menjadi dasar untuk penelitian lanjutan dengan cakupan sampel yang lebih luas dan validasi tambahan pada wilayah di luar lokasi pengembangan model.

### 1.6 Ruang Lingkup dan Batasan Penelitian

**Ruang Lingkup Wilayah Penelitian**

Penelitian ini berfokus pada klasifikasi tutupan lahan dengan target penerapan pada wilayah Provinsi Jawa Timur. Namun, pengambilan sampel berlabel dan analisis raster pada penelitian ini difokuskan pada wilayah Muncar, Teluk Pangpang, Tegaldlimo, dan sekitarnya di Kabupaten Banyuwangi. Oleh karena itu, hasil evaluasi model merepresentasikan kinerja pada sampel yang digunakan di wilayah studi tersebut dan belum dapat dianggap mewakili seluruh wilayah Provinsi Jawa Timur.

## 2. Data Understanding

Tahap *Data Understanding* bertujuan memahami karakteristik data yang digunakan dalam klasifikasi tutupan lahan. Data terdiri atas dua komponen utama: poligon sampel tutupan lahan hasil digitasi manual dan citra satelit Sentinel-2 Level-2A dari Copernicus Data Space Ecosystem.

Poligon sampel mencakup lima kelas tutupan lahan, yaitu kawasan terbangun (*built-up*), lahan pertanian (*farmland*), badan air (*water body*), hutan non-mangrove (*forest*), dan hutan mangrove (*mangrove*). Digitasi dilakukan pada wilayah Muncar, Teluk Pangpang, Tegaldlimo, dan sekitarnya di Kabupaten Banyuwangi, Jawa Timur. Citra Sentinel-2 digunakan untuk memperoleh informasi spektral yang menghubungkan setiap poligon sampel dengan nilai reflektansi permukaan bumi.

### 2.1 Pengumpulan dan Pemahaman Data

Data referensi tutupan lahan diperoleh melalui digitasi poligon secara manual menggunakan citra acuan. Setiap poligon diberi label identitas yang menunjukkan kelasnya, seperti `build1`, `farm1`, `water1`, `forest1`, dan `mang1`. Data ini disimpan dalam format GeoJSON dan menjadi satu-satunya sumber ground truth yang digunakan dalam penelitian.

Data citra menggunakan Sentinel-2 Level-2A dari Copernicus Data Space Ecosystem melalui antarmuka openEO. Koleksi yang digunakan adalah `SENTINEL2_L2A`. Band yang diprioritaskan adalah B03 (*Green*), B04 (*Red*), B08 (*Near Infrared*), dan B11 (*Shortwave Infrared*). Resolusi kerja yang direncanakan adalah 20 meter karena band B11 memiliki resolusi asli 20 meter.

Sel berikut memeriksa keberadaan file GeoJSON sebelum data dibaca.


```python
from pathlib import Path

file_geojson = Path(
    r"C:\Users\Alif\PSD\build,farm,water,forest,mangrove.geojson"
)

print("File ditemukan:", file_geojson.exists())
print("Path:", file_geojson)

if file_geojson.exists():
    print("Ukuran file:", f"{file_geojson.stat().st_size:,} bytes")
else:
    print("File tidak ditemukan. Periksa kembali lokasi file.")
```

    File ditemukan: True
    Path: C:\Users\Alif\PSD\build,farm,water,forest,mangrove.geojson
    Ukuran file: 114,806 bytes
    

### 2.2 Pemeriksaan dan Kualitas Data Sampel

Pemeriksaan data sampel dilakukan untuk mengetahui jumlah fitur, struktur atribut, distribusi label per kelas, kualitas geometri, dan sistem koordinat. Tahap ini penting untuk memastikan data referensi siap digunakan sebelum memasuki tahap *Data Preparation*.

**Langkah pemeriksaan:**
1. Pembacaan data GeoJSON dan identifikasi jumlah fitur serta jenis geometri
2. Penyeragaman label ke lima kelas dan deteksi fitur tanpa label
3. Pemeriksaan kualitas geometri: keberadaan, validitas, dan luas
4. Identifikasi fitur bermasalah dan penanganannya
5. Penetapan dan verifikasi sistem koordinat (CRS)


```python
import json
import re
from collections import Counter
from pathlib import Path

# Baca data GeoJSON (data asli tidak diubah)
file_geojson = Path(
    r"C:\Users\Alif\PSD\build,farm,water,forest,mangrove.geojson"
)

with file_geojson.open("r", encoding="utf-8") as file:
    data_geojson = json.load(file)

features = data_geojson.get("features", [])
print("Jumlah fitur:", len(features))

# Distribusi label mentah
print("\nDistribusi label:")
label_counts = Counter(
    str(feature.get("properties", {}).get("class", "")).strip()
    for feature in features
)
for label, jumlah in sorted(label_counts.items()):
    print(f"{label or '[tanpa label]'}: {jumlah}")

# Jenis geometri
print("\nJenis geometri:")
geometry_counts = Counter(
    (feature.get("geometry") or {}).get("type", "Tidak tersedia")
    for feature in features
)
for jenis, jumlah in sorted(geometry_counts.items()):
    print(f"{jenis}: {jumlah}")

# Contoh atribut
print("\nContoh atribut:")
for feature in features[:3]:
    print(feature.get("properties", {}))
```

    Jumlah fitur: 508
    
    Distribusi label:
    [tanpa label]: 1
    build 5: 1
    build1: 1
    build10: 1
    build100: 1
    build11: 1
    build12: 1
    build13: 1
    build14: 1
    build15: 1
    build16: 1
    build17: 1
    build18: 1
    build19: 1
    build2: 1
    build20: 1
    build21: 1
    build22: 1
    build23: 1
    build24: 1
    build25: 1
    build26: 1
    build27: 1
    build28: 1
    build29: 1
    build3: 1
    build30: 1
    build31: 1
    build32: 1
    build33: 1
    build34: 1
    build35: 1
    build36: 1
    build37: 1
    build38: 1
    build39: 1
    build4: 1
    build40: 1
    build41: 1
    build42: 1
    build43: 1
    build44: 1
    build45: 2
    build46: 1
    build47: 1
    build48: 1
    build49: 1
    build50: 1
    build51: 1
    build52: 1
    build53: 1
    build54: 1
    build55: 1
    build56: 1
    build57: 1
    build58: 1
    build59: 1
    build6: 1
    build60: 1
    build61: 1
    build62: 1
    build63: 1
    build64: 1
    build65: 1
    build66: 1
    build67: 1
    build68: 1
    build69: 1
    build7: 1
    build70: 1
    build71: 1
    build72: 1
    build73: 1
    build74: 1
    build75: 1
    build76: 1
    build77: 1
    build78: 1
    build79: 1
    build8: 1
    build80: 1
    build81: 1
    build82: 1
    build83: 1
    build84: 1
    build85: 1
    build86: 1
    build87: 1
    build88: 1
    build89: 1
    build9: 1
    build90: 1
    build91: 1
    build92: 1
    build93: 1
    build94: 1
    build95: 1
    build96: 1
    build97: 1
    build98: 1
    build99: 1
    farm1: 1
    farm10: 1
    farm100: 1
    farm11: 1
    farm12: 1
    farm13: 1
    farm14: 1
    farm15: 1
    farm16: 1
    farm17: 1
    farm18: 1
    farm19: 1
    farm2: 1
    farm20: 1
    farm21: 1
    farm22: 1
    farm23: 1
    farm24: 1
    farm25: 1
    farm26: 1
    farm27: 1
    farm28: 1
    farm29: 1
    farm3: 1
    farm30: 1
    farm31: 1
    farm32: 1
    farm33: 1
    farm34: 1
    farm35: 1
    farm36: 1
    farm37: 1
    farm38: 1
    farm39: 1
    farm4: 1
    farm40: 1
    farm41: 1
    farm42: 1
    farm43: 1
    farm44: 1
    farm45: 1
    farm46: 1
    farm47: 1
    farm48: 1
    farm49: 1
    farm5: 1
    farm50: 1
    farm51: 1
    farm52: 1
    farm53: 1
    farm54: 1
    farm55: 1
    farm56: 1
    farm57: 1
    farm58: 1
    farm59: 1
    farm6: 1
    farm60: 1
    farm61: 1
    farm62: 1
    farm63: 1
    farm64: 1
    farm65: 1
    farm66: 1
    farm67: 1
    farm68: 1
    farm69: 1
    farm7: 1
    farm70: 1
    farm71: 1
    farm72: 1
    farm73: 1
    farm74: 1
    farm75: 1
    farm76: 1
    farm77: 1
    farm78: 1
    farm79: 1
    farm8: 1
    farm80: 1
    farm81: 1
    farm82: 1
    farm83: 1
    farm84: 1
    farm85: 1
    farm86: 1
    farm87: 1
    farm88: 1
    farm89: 1
    farm9: 1
    farm90: 1
    farm91: 1
    farm92: 1
    farm93: 1
    farm94: 1
    farm95: 1
    farm96: 1
    farm97: 1
    farm98: 1
    farm99: 1
    forest1: 1
    forest10: 1
    forest100: 1
    forest11: 1
    forest12: 1
    forest13: 1
    forest14: 1
    forest15: 1
    forest16: 1
    forest17: 1
    forest18: 1
    forest19: 1
    forest2: 1
    forest20: 1
    forest21: 1
    forest22: 1
    forest23: 1
    forest24: 1
    forest25: 1
    forest26: 1
    forest27: 1
    forest28: 1
    forest29: 1
    forest3: 1
    forest30: 1
    forest31: 1
    forest32: 1
    forest33: 1
    forest34: 1
    forest35: 1
    forest36: 1
    forest37: 1
    forest38: 1
    forest39: 1
    forest4: 1
    forest40: 1
    forest41: 1
    forest42: 1
    forest43: 1
    forest44: 1
    forest45: 1
    forest46: 1
    forest47: 1
    forest48: 1
    forest49: 1
    forest5: 1
    forest50: 1
    forest51: 1
    forest52: 1
    forest53: 1
    forest54: 1
    forest55: 1
    forest56: 1
    forest57: 1
    forest58: 1
    forest59: 1
    forest6: 1
    forest60: 1
    forest61: 1
    forest62: 1
    forest63: 1
    forest64: 1
    forest65: 1
    forest66: 1
    forest67: 1
    forest68: 1
    forest69: 1
    forest7: 1
    forest70: 1
    forest71: 1
    forest72: 1
    forest73: 1
    forest74: 1
    forest75: 1
    forest76: 1
    forest77: 1
    forest78: 1
    forest79: 1
    forest8: 1
    forest80: 1
    forest81: 1
    forest82: 1
    forest83: 1
    forest84: 1
    forest85: 1
    forest86: 1
    forest87: 1
    forest88: 1
    forest89: 1
    forest9: 1
    forest90: 1
    forest91: 1
    forest92: 1
    forest93: 1
    forest94: 1
    forest95: 1
    forest96: 1
    forest97: 1
    forest98: 1
    forest99: 1
    mang1: 1
    mang10: 1
    mang100: 1
    mang11: 1
    mang12: 1
    mang13: 1
    mang14: 1
    mang15: 1
    mang16: 1
    mang17: 1
    mang18: 1
    mang19: 1
    mang2: 1
    mang20: 1
    mang21: 1
    mang22: 1
    mang23: 1
    mang24: 1
    mang25: 1
    mang26: 1
    mang27: 1
    mang28: 1
    mang29: 1
    mang3: 1
    mang30: 1
    mang31: 1
    mang32: 1
    mang33: 1
    mang34: 1
    mang35: 1
    mang36: 1
    mang37: 1
    mang38: 1
    mang39: 1
    mang4: 1
    mang40: 1
    mang41: 1
    mang42: 1
    mang43: 1
    mang44: 1
    mang45: 1
    mang46: 1
    mang47: 1
    mang48: 1
    mang49: 1
    mang5: 1
    mang50: 1
    mang51: 1
    mang52: 1
    mang53: 1
    mang54: 3
    mang55: 1
    mang56: 1
    mang57: 1
    mang58: 1
    mang59: 1
    mang6: 1
    mang60: 1
    mang61: 1
    mang62: 1
    mang63: 1
    mang64: 2
    mang65: 1
    mang66: 1
    mang67: 1
    mang68: 1
    mang69: 1
    mang7: 1
    mang70: 1
    mang71: 1
    mang72: 1
    mang73: 1
    mang74: 2
    mang75: 1
    mang76: 1
    mang77: 1
    mang78: 1
    mang79: 1
    mang8: 1
    mang80: 1
    mang81: 1
    mang82: 1
    mang83: 1
    mang84: 1
    mang85: 1
    mang86: 1
    mang87: 1
    mang88: 1
    mang89: 1
    mang9: 1
    mang90: 1
    mang91: 1
    mang92: 1
    mang93: 1
    mang94: 1
    mang95: 1
    mang96: 1
    mang97: 1
    mang98: 1
    mang99: 1
    water1: 1
    water10: 1
    water100: 1
    water11: 1
    water12: 1
    water13: 1
    water14: 1
    water15: 1
    water16: 1
    water17: 1
    water18: 1
    water19: 1
    water2: 1
    water20: 1
    water21: 1
    water22: 2
    water23: 1
    water24: 1
    water25: 1
    water26: 1
    water27: 1
    water28: 2
    water29: 1
    water3: 1
    water30: 1
    water31: 1
    water32: 1
    water33: 1
    water34: 1
    water35: 1
    water36: 1
    water37: 1
    water38: 1
    water39: 1
    water4: 1
    water40: 1
    water41: 1
    water42: 1
    water43: 1
    water44: 1
    water45: 1
    water46: 1
    water47: 1
    water48: 1
    water49: 1
    water5: 1
    water50: 1
    water51: 1
    water52: 1
    water53: 1
    water54: 1
    water55: 1
    water56: 1
    water57: 1
    water58: 1
    water59: 1
    water6: 1
    water60: 1
    water61: 1
    water62: 1
    water63: 1
    water64: 1
    water65: 1
    water66: 1
    water67: 1
    water68: 1
    water69: 1
    water7: 1
    water70: 1
    water71: 1
    water72: 1
    water73: 1
    water74: 1
    water75: 1
    water76: 1
    water77: 1
    water78: 1
    water79: 1
    water8: 1
    water80: 1
    water81: 1
    water82: 1
    water83: 1
    water84: 1
    water85: 1
    water86: 1
    water87: 1
    water88: 1
    water89: 1
    water9: 1
    water90: 1
    water91: 1
    water92: 1
    water93: 1
    water94: 1
    water95: 1
    water96: 1
    water97: 1
    water98: 1
    water99: 1
    
    Jenis geometri:
    Polygon: 508
    
    Contoh atribut:
    {'class': 'build1'}
    {'class': 'build2'}
    {'class': 'build3'}
    

#### Penyeragaman Label ke Lima Kelas

Atribut `class` berisi identitas unik per poligon (misalnya `build1`, `mang40`). Label tersebut dipetakan ke lima kelas tutupan lahan berdasarkan awalan:

| Awalan label | Kelas tutupan lahan |
|:------------|:--------------------|
| `build` + nomor | `built_up` |
| `farm` + nomor | `farmland` |
| `water` + nomor | `water_body` |
| `forest` + nomor | `forest` |
| `mang` + nomor | `mangrove` |

Fitur tanpa label atau label tidak dikenali dicatat terpisah.


```python
def tentukan_kelas(label):
    """Petakan label identitas poligon ke nama kelas tutupan lahan."""
    label = str(label).strip().lower()

    if re.fullmatch(r"build\s*\d*", label):
        return "built_up"
    elif re.fullmatch(r"farm\s*\d*", label):
        return "farmland"
    elif re.fullmatch(r"water\s*\d*", label):
        return "water_body"
    elif re.fullmatch(r"forest\s*\d*", label):
        return "forest"
    elif re.fullmatch(r"mang\s*\d*", label):
        return "mangrove"
    else:
        return None


ringkasan_kelas = Counter()
tanpa_label = 0
label_tidak_dikenali = []

for feature in features:
    label_asli = feature.get("properties", {}).get("class")
    kelas = tentukan_kelas(label_asli or "")

    if kelas is None:
        if not str(label_asli or "").strip():
            tanpa_label += 1
        else:
            label_tidak_dikenali.append(label_asli)
    else:
        ringkasan_kelas[kelas] += 1

print("Distribusi lima kelas (sebelum pembersihan geometri):")
for kelas in ["built_up", "farmland", "water_body", "forest", "mangrove"]:
    print(f"{kelas}: {ringkasan_kelas[kelas]}")

print("\nFitur tanpa label:", tanpa_label)
print("Label tidak dikenali:", label_tidak_dikenali)
```

    Distribusi lima kelas (sebelum pembersihan geometri):
    built_up: 101
    farmland: 100
    water_body: 102
    forest: 100
    mangrove: 104
    
    Fitur tanpa label: 1
    Label tidak dikenali: []
    

#### Pemeriksaan Kualitas Geometri

Pemeriksaan geometri menggunakan Shapely untuk mengidentifikasi: geometri kosong, geometri tidak valid (*self-intersection*), geometri berluas nol, dan fitur yang gagal diparse. Data asli GeoJSON **tidak diubah** pada tahap ini.


```python
from shapely.geometry import shape

jumlah_geometri_kosong = 0
jumlah_geometri_tidak_valid = 0
jumlah_luas_nol = 0
jenis_geometri = Counter()
masalah_geometri = []

for i, feature in enumerate(features):
    geom_json = feature.get("geometry")

    if not geom_json:
        jumlah_geometri_kosong += 1
        masalah_geometri.append((i, "Geometri kosong"))
        continue

    try:
        geom = shape(geom_json)
        jenis_geometri[geom.geom_type] += 1

        if not geom.is_valid:
            jumlah_geometri_tidak_valid += 1
            masalah_geometri.append((i, "Geometri tidak valid"))

        if geom.is_empty:
            jumlah_geometri_kosong += 1
            masalah_geometri.append((i, "Geometri kosong"))
        elif geom.area == 0:
            jumlah_luas_nol += 1
            masalah_geometri.append((i, "Luas geometri nol"))

    except Exception as error:
        masalah_geometri.append((i, f"Gagal dibaca: {error}"))

print("Jumlah fitur:", len(features))
print("Jenis geometri:", dict(jenis_geometri))
print("Geometri kosong:", jumlah_geometri_kosong)
print("Geometri tidak valid:", jumlah_geometri_tidak_valid)
print("Luas geometri nol:", jumlah_luas_nol)
print("Jumlah fitur bermasalah:", len(masalah_geometri))

if masalah_geometri:
    print("\nContoh fitur bermasalah:")
    for masalah in masalah_geometri[:10]:
        print(masalah)
```

    Jumlah fitur: 508
    Jenis geometri: {'Polygon': 507}
    Geometri kosong: 0
    Geometri tidak valid: 1
    Luas geometri nol: 0
    Jumlah fitur bermasalah: 2
    
    Contoh fitur bermasalah:
    (442, 'Geometri tidak valid')
    (448, 'Gagal dibaca: A linearring requires at least 4 coordinates.')
    


```python
# Tampilkan detail setiap fitur bermasalah untuk pemeriksaan manual
for indeks, keterangan in masalah_geometri:
    feature = features[indeks]
    print(f"\nIndeks fitur: {indeks}")
    print("Masalah:", keterangan)
    print("Atribut:", feature.get("properties", {}))
    print("Geometri:", feature.get("geometry"))
```

    
    Indeks fitur: 442
    Masalah: Geometri tidak valid
    Atribut: {'class': 'mang40'}
    Geometri: {'type': 'Polygon', 'coordinates': [[[114.36704, -8.475842], [114.366909, -8.475674], [114.366913, -8.475677], [114.366909, -8.475674], [114.366909, -8.47567], [114.367214, -8.476043], [114.367497, -8.476187], [114.367824, -8.476051], [114.367305, -8.475512], [114.366909, -8.47567], [114.36704, -8.475842]]]}
    
    Indeks fitur: 448
    Masalah: Gagal dibaca: A linearring requires at least 4 coordinates.
    Atribut: {}
    Geometri: {'type': 'Polygon', 'coordinates': [[[114.363712, -8.476711], [114.363712, -8.476711]]]}
    

#### Hasil Pemeriksaan Fitur Bermasalah

**Fitur indeks 442 — `mang40`:** Geometri tidak valid karena *self-intersection* (titik berulang yang membentuk simpul). Percobaan perbaikan dengan `shapely.make_valid()` menghasilkan `GeometryCollection`, bukan `Polygon`/`MultiPolygon`. Karena hasil perbaikan tidak menghasilkan geometri poligon yang dapat digunakan untuk rasterisasi, fitur ini **dikecualikan** dan dicatat sebagai keterbatasan data.

**Fitur indeks 448:** Tidak memiliki atribut kelas (label kosong) dan geometri hanya berisi dua titik koordinat yang sama — tidak dapat membentuk *linear ring* yang valid. Fitur ini **dikecualikan** karena tidak memiliki kelas referensi dan geometri tidak dapat diperbaiki.

Dari 508 fitur awal, **506 fitur** layak digunakan untuk analisis lebih lanjut.


```python
from shapely.geometry import shape, mapping
from shapely import make_valid

features_bersih = []
fitur_dikecualikan = []

for indeks, feature in enumerate(features):
    geom_json = feature.get("geometry")

    try:
        if not geom_json:
            raise ValueError("Geometri kosong")

        geom = shape(geom_json)

        if not geom.is_valid:
            geom = make_valid(geom)

        if geom.is_empty or geom.area == 0:
            raise ValueError("Geometri kosong atau luas nol")

        # make_valid dapat menghasilkan GeometryCollection pada geometri
        # dengan self-intersection kompleks — dikecualikan jika bukan Polygon/MultiPolygon
        if geom.geom_type not in ["Polygon", "MultiPolygon"]:
            raise ValueError(
                f"Jenis geometri tidak sesuai setelah make_valid: {geom.geom_type}"
            )

        feature_baru = {**feature, "geometry": mapping(geom)}
        features_bersih.append(feature_baru)

    except Exception as error:
        fitur_dikecualikan.append({
            "indeks": indeks,
            "alasan": str(error),
            "atribut": feature.get("properties", {})
        })

print("Fitur awal:", len(features))
print("Fitur yang dapat digunakan:", len(features_bersih))
print("Fitur yang dikecualikan:", len(fitur_dikecualikan))
for item in fitur_dikecualikan:
    print(item)

# Rekap distribusi kelas setelah pembersihan
jumlah_kelas = Counter()
for feature in features_bersih:
    label = feature.get("properties", {}).get("class", "")
    kelas = tentukan_kelas(label)
    if kelas:
        jumlah_kelas[kelas] += 1

print("\nDistribusi kelas setelah pembersihan:")
for kelas in ["built_up", "farmland", "water_body", "forest", "mangrove"]:
    print(f"{kelas}: {jumlah_kelas[kelas]}")
```

    Fitur awal: 508
    Fitur yang dapat digunakan: 506
    Fitur yang dikecualikan: 2
    {'indeks': 442, 'alasan': 'Jenis geometri tidak sesuai setelah make_valid: GeometryCollection', 'atribut': {'class': 'mang40'}}
    {'indeks': 448, 'alasan': 'A linearring requires at least 4 coordinates.', 'atribut': {}}
    
    Distribusi kelas setelah pembersihan:
    built_up: 101
    farmland: 100
    water_body: 102
    forest: 100
    mangrove: 103
    

#### Penetapan dan Verifikasi Sistem Koordinat (CRS)

GeoJSON standar menggunakan koordinat geografis WGS84 (EPSG:4326). Berdasarkan rentang koordinat data (bujur ≈ 114.34–114.58, lintang ≈ -8.44 hingga -8.70), lokasi sampel sesuai dengan wilayah Kabupaten Banyuwangi, Jawa Timur.

Metadata CRS tidak tersimpan dalam file GeoJSON (mengembalikan `None`). Penetapan CRS dilakukan dengan `set_crs('EPSG:4326')` karena koordinat sudah dalam format geografis WGS84. Ini **bukan reproyeksi** — nilai koordinat tidak berubah, hanya referensi CRS yang ditambahkan pada GeoDataFrame.


```python
import geopandas as gpd

# Buat GeoDataFrame dari fitur yang sudah bersih
gdf_sampel = gpd.GeoDataFrame(
    [
        {
            **feature.get("properties", {}),
            "geometry": shape(feature["geometry"])
        }
        for feature in features_bersih
    ],
    crs=data_geojson.get("crs", {}).get("properties", {}).get("name")
)

print("CRS dari metadata GeoJSON:", gdf_sampel.crs)

# Tetapkan CRS WGS84 — bukan reproyeksi, koordinat tidak berubah
gdf_sampel = gdf_sampel.set_crs("EPSG:4326", allow_override=True)

print("CRS setelah ditetapkan:", gdf_sampel.crs)
print("Jumlah sampel:", len(gdf_sampel))

minx, miny, maxx, maxy = gdf_sampel.total_bounds
print(f"Batas koordinat — Bujur: {minx:.4f} hingga {maxx:.4f}")
print(f"Batas koordinat — Lintang: {miny:.4f} hingga {maxy:.4f}")
print("Wilayah: Banyuwangi (Muncar, Teluk Pangpang, Tegaldlimo)")
```

    CRS dari metadata GeoJSON: None
    CRS setelah ditetapkan: EPSG:4326
    Jumlah sampel: 506
    Batas koordinat — Bujur: 114.3365 hingga 114.5801
    Batas koordinat — Lintang: -8.7016 hingga -8.4363
    Wilayah: Banyuwangi (Muncar, Teluk Pangpang, Tegaldlimo)
    

### 2.3 Pengambilan dan Pemeriksaan Citra Sentinel-2

Citra Sentinel-2 Level-2A diperoleh melalui Copernicus Data Space Ecosystem menggunakan antarmuka openEO. Koleksi yang digunakan adalah `SENTINEL2_L2A`. Band yang diperlukan adalah **B03** (*Green*), **B04** (*Red*), **B08** (*NIR*), dan **B11** (*SWIR*). Resolusi kerja 20 meter dipilih karena band B11 memiliki resolusi asli 20 meter.

Wilayah pengambilan citra (AOI) ditentukan berdasarkan batas poligon sampel ditambah buffer ≈1 km. Periode pengamatan dipilih dengan mempertimbangkan ketersediaan citra dan minimnya tutupan awan.

**Urutan langkah pada subbab ini:**
1. Hitung AOI dari batas poligon sampel
2. Periksa versi dan status koneksi openEO
3. Autentikasi ke Copernicus Data Space (memerlukan akun aktif)
4. Verifikasi ketersediaan koleksi `SENTINEL2_L2A`
5. Definisi proses pengambilan citra (belum dieksekusi)


```python
import math

# Tentukan AOI berdasarkan batas poligon sampel
gdf_aoi = gdf_sampel.to_crs("EPSG:4326")
min_lon, min_lat, max_lon, max_lat = gdf_aoi.total_bounds

# Buffer ~1 km dalam derajat
buffer_lat = 1 / 111
buffer_lon = 1 / (111 * abs(math.cos(math.radians((min_lat + max_lat) / 2))))

bbox = {
    "west": round(min_lon - buffer_lon, 4),
    "south": round(min_lat - buffer_lat, 4),
    "east": round(max_lon + buffer_lon, 4),
    "north": round(max_lat + buffer_lat, 4)
}

print("Batas wilayah pengambilan citra (AOI dengan buffer ~1 km):")
print(bbox)
print("\nJumlah poligon referensi:", len(gdf_sampel))
print("CRS poligon:", gdf_sampel.crs)
```

    Batas wilayah pengambilan citra (AOI dengan buffer ~1 km):
    {'west': np.float64(114.3274), 'south': np.float64(-8.7106), 'east': np.float64(114.5892), 'north': np.float64(-8.4273)}
    
    Jumlah poligon referensi: 506
    CRS poligon: EPSG:4326
    


```python
import openeo

print("Versi openEO:", openeo.__version__)
print("Tipe koneksi:", type(connection))
print("Endpoint:", getattr(connection, "url", "Tidak tersedia"))
print("Method autentikasi tersedia:", hasattr(connection, "authenticate_oidc"))
```

    Versi openEO: 0.50.0
    Tipe koneksi: <class 'openeo.rest.connection.Connection'>
    Endpoint: Tidak tersedia
    Method autentikasi tersedia: True
    

#### Autentikasi Copernicus Data Space Ecosystem

Autentikasi diperlukan untuk mengakses layanan pemrosesan citra openEO. Jika token dari sesi sebelumnya masih valid, autentikasi menggunakan *refresh token* secara otomatis. Jika sesi baru, browser akan terbuka untuk login.

> **Tindakan pengguna:** Jalankan sel ini. Ikuti instruksi browser jika halaman login muncul. Setelah berhasil, lanjutkan ke sel verifikasi koleksi.


```python
connection.authenticate_oidc()
```

    Authenticated using refresh token.
    




    <Connection to 'https://openeo.dataspace.copernicus.eu/openeo/1.2/' with OidcBearerAuth>




```python
# Verifikasi ketersediaan koleksi SENTINEL2_L2A
collection_ids = connection.list_collection_ids()

print("Koleksi SENTINEL2_L2A tersedia:", "SENTINEL2_L2A" in collection_ids)

print("\nKoleksi terkait Sentinel-2:")
for collection_id in collection_ids:
    if "SENTINEL2" in collection_id.upper():
        print(collection_id)
```

    Koleksi SENTINEL2_L2A tersedia: True
    
    Koleksi terkait Sentinel-2:
    SENTINEL2_L2A
    SENTINEL2_L1C
    

#### Definisi Proses Pengambilan Citra

Sel berikut mendefinisikan alur pengambilan citra menggunakan openEO (*lazy evaluation*). **Proses ini belum mengunduh data** — eksekusi download dilakukan pada tahap *Data Preparation*.

**Parameter:**
- Koleksi: `SENTINEL2_L2A`
- Band: `B03`, `B04`, `B08`, `B11`
- Periode: musim kemarau (Juli–September) untuk meminimalkan tutupan awan
- AOI: batas wilayah dari poligon sampel dengan buffer ≈1 km
- Resolusi rencana: 20 meter

> **Catatan:** Jangan klaim citra berhasil diunduh sebelum proses `.download()` atau `.execute_batch()` selesai dan file keluaran diverifikasi.


```python
# Definisi proses pengambilan citra Sentinel-2 melalui openEO
# Sel ini hanya mendefinisikan alur (lazy evaluation) — belum mengunduh data
# Jalankan setelah autentikasi berhasil

import openeo

# Hubungkan ke Copernicus Data Space Ecosystem (gunakan koneksi aktif jika tersedia)
connection = openeo.connect("https://openeo.dataspace.copernicus.eu")

# Spatial extent dari AOI
spatial_extent = {
    "west": bbox["west"],
    "south": bbox["south"],
    "east": bbox["east"],
    "north": bbox["north"],
    "crs": "EPSG:4326"
}

# Definisi proses (belum dieksekusi)
datacube = connection.load_collection(
    collection_id="SENTINEL2_L2A",
    spatial_extent=spatial_extent,
    temporal_extent=["2024-07-01", "2024-09-30"],
    bands=["B03", "B04", "B08", "B11"]
)

print("Datacube berhasil didefinisikan (belum dieksekusi):")
print(type(datacube))
print("\nBand yang diminta:", ["B03", "B04", "B08", "B11"])
print("Resolusi rencana: 20 meter")
print("\nCATATAN: Download belum dilakukan.")
print("Lanjutkan ke Bab 3 (Data Preparation) untuk eksekusi .download() atau .execute_batch().")
```

    Datacube berhasil didefinisikan (belum dieksekusi):
    <class 'openeo.rest.datacube.DataCube'>
    
    Band yang diminta: ['B03', 'B04', 'B08', 'B11']
    Resolusi rencana: 20 meter
    
    CATATAN: Download belum dilakukan.
    Lanjutkan ke Bab 3 (Data Preparation) untuk eksekusi .download() atau .execute_batch().
    

## 3. Data Preparation

Tahap *Data Preparation* bertujuan mengolah data mentah dari Bab 2 menjadi dataset terstruktur berkualitas tinggi yang siap digunakan untuk pemodelan klasifikasi tutupan lahan pada Bab 4. Berdasarkan keputusan metodologis proyek dan audit CRISP-DM, persiapan data mencakup penanganan kualitas sampel spasial, audit metadata citra satelit dan penetapan periode temporal, prapemrosesan radiometrik/masking, ekstraksi fitur spektral berdasar piksel valid, serta pembagian data latih-uji yang bebas kebocoran (*data leakage*).

Seluruh pengolahan pada bab ini didasarkan pada batasan teknis:
- **Wilayah studi**: Kecamatan Muncar, Teluk Pangpang, Tegaldlimo, dan sekitarnya (Kabupaten Banyuwangi, Jawa Timur).
- **Data sampel**: Poligon ground truth dari `build,farm,water,forest,mangrove.geojson` (5 kelas target).
- **Keputusan Citra dan Periode:** Periode target penelitian ditetapkan pada 1 Januari 2025 hingga 31 Desember 2025. Namun, berdasarkan audit metadata pada `hasil_sentinel2/job-results.json` dan raster `hasil_sentinel2/openEO.tif`, citra yang tersedia dan digunakan dalam pengujian memiliki rentang akuisisi aktual 5 Desember 2025 hingga 8 Oktober 2026. Dengan demikian, raster yang digunakan belum merepresentasikan komposit tahunan penuh 2025. Keterbatasan periode ini diperhitungkan dalam interpretasi hasil penelitian.
- **Indeks spektral**: NDVI, NDWI, dan NDBI dihitung secara konsisten per piksel valid sebelum diagregasikan ke tingkat poligon.
- **Pembagian data**: 70% data latih dan 30% data uji berbasis identitas poligon (*polygon-level stratified split*).

### 3.1 Persiapan dan Pembersihan Data Sampel

Tahap ini memuat data vektor GeoJSON ground truth secara mandiri (*self-contained*), menormalkan penamaan label ke dalam 5 kelas standar, memvalidasi geometri menggunakan `shapely.make_valid`, menyaring geometri invalid/kosong, dan memverifikasi batas spasial.

**Aturan Penanganan Sampel:**
- File sumber GeoJSON asli (`build,farm,water,forest,mangrove.geojson`) dibaca secara *read-only* tanpa modifikasi fisik.
- Label kelas dipetakan secara deterministik via *regex*: `built_up` (pola `build*`), `farmland` (`farm*`), `water_body` (`water*`), `forest` (`forest*`), dan `mangrove` (`mang*`).
- Sampel dengan label kosong atau geometri yang tidak dapat direparasi menjadi poligon valid (`Polygon`/`MultiPolygon`) dikecualikan secara transparan dan dicatat alasannya.


```python
import json
import re
from collections import Counter
from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely.geometry import shape, mapping
from shapely import make_valid

# --- Muat data GeoJSON asli (read-only) ---
FILE_GEOJSON = Path(r'C:\Users\Alif\PSD\build,farm,water,forest,mangrove.geojson')
assert FILE_GEOJSON.exists(), f'GeoJSON tidak ditemukan: {FILE_GEOJSON}'

with FILE_GEOJSON.open('r', encoding='utf-8') as f:
    data_geojson = json.load(f)

features_raw = data_geojson.get('features', [])
print(f'Total fitur mentah dalam GeoJSON: {len(features_raw)}')


# --- Fungsi pemetaan label ke 5 kelas standar ---
def tentukan_kelas(label: str):
    label = str(label).strip().lower()
    if re.fullmatch(r'build\s*\d*', label):  return 'built_up'
    if re.fullmatch(r'farm\s*\d*',  label):  return 'farmland'
    if re.fullmatch(r'water\s*\d*', label):  return 'water_body'
    if re.fullmatch(r'forest\s*\d*',label):  return 'forest'
    if re.fullmatch(r'mang\s*\d*',  label):  return 'mangrove'
    return None


# --- Pembersihan dan validasi geometri ---
features_bersih = []
dikecualikan = []

for idx, feat in enumerate(features_raw):
    props    = feat.get('properties', {})
    label    = props.get('class', '')
    kelas    = tentukan_kelas(label or '')
    geom_raw = feat.get('geometry')

    # Validasi label
    if kelas is None:
        alasan = 'Label kosong' if not str(label).strip() else f'Label tidak dikenali: {label}'
        dikecualikan.append({'indeks': idx, 'label_asli': label, 'kelas': None, 'alasan': alasan})
        continue

    # Validasi keberadaan geometri
    if not geom_raw:
        dikecualikan.append({'indeks': idx, 'label_asli': label, 'kelas': kelas, 'alasan': 'Geometri kosong (None)'})
        continue

    try:
        geom = shape(geom_raw)
    except Exception as e:
        dikecualikan.append({'indeks': idx, 'label_asli': label, 'kelas': kelas, 'alasan': f'Gagal parsing geometri: {e}'})
        continue

    # Reparasi geometri jika invalid
    if not geom.is_valid:
        geom = make_valid(geom)

    if geom.is_empty or geom.area == 0:
        dikecualikan.append({'indeks': idx, 'label_asli': label, 'kelas': kelas, 'alasan': 'Geometri kosong atau luas nol'})
        continue

    if geom.geom_type not in ('Polygon', 'MultiPolygon'):
        dikecualikan.append({'indeks': idx, 'label_asli': label, 'kelas': kelas,
                             'alasan': f'Tipe geometri tidak didukung ({geom.geom_type})'})
        continue

    features_bersih.append({
        'polygon_id': idx,
        'label_asli': label,
        'kelas': kelas,
        'geometry': geom
    })

# Konstruksi GeoDataFrame CRS EPSG:4326 (WGS84 Standar GeoJSON)
gdf_sampel = gpd.GeoDataFrame(features_bersih, crs='EPSG:4326')

# --- Laporan Pembersihan Data Sampel ---
print(f'Fitur valid lolos seleksi: {len(gdf_sampel)}')
print(f'Fitur dikecualikan      : {len(dikecualikan)}')
print('\nRincian fitur dikecualikan:')
for d in dikecualikan:
    print(f"  Index {d['indeks']:3d} | Label: '{d['label_asli']}' | Alasan: {d['alasan']}")

print('\nDistribusi kelas sampel valid:')
dist = Counter(gdf_sampel['kelas'])
for k in ['built_up', 'farmland', 'water_body', 'forest', 'mangrove']:
    print(f'  {k:12s}: {dist[k]:3d} poligon')
print(f'  {"Total":12s}: {sum(dist.values()):3d} poligon')

minx, miny, maxx, maxy = gdf_sampel.total_bounds
print(f'\nCRS data sampel : {gdf_sampel.crs}')
print(f'Batas koordinat : Barat={minx:.4f}, Selatan={miny:.4f}, Timur={maxx:.4f}, Utara={maxy:.4f}')
```

    Total fitur mentah dalam GeoJSON: 508
    Fitur valid lolos seleksi: 506
    Fitur dikecualikan      : 2
    
    Rincian fitur dikecualikan:
      Index 442 | Label: 'mang40' | Alasan: Tipe geometri tidak didukung (GeometryCollection)
      Index 448 | Label: '' | Alasan: Label kosong
    
    Distribusi kelas sampel valid:
      built_up    : 101 poligon
      farmland    : 100 poligon
      water_body  : 102 poligon
      forest      : 100 poligon
      mangrove    : 103 poligon
      Total       : 506 poligon
    
    CRS data sampel : EPSG:4326
    Batas koordinat : Barat=114.3365, Selatan=-8.7016, Timur=114.5801, Utara=-8.4363
    

### 3.2 Penetapan Periode Penelitian 2025 dan Audit Metadata Citra openEO

#### 1. Keputusan Periode Pengamatan (1 Januari 2025 – 31 Desember 2025)
Sesuai arahan metodologi, periode penelitian ditetapkan menjadi **1 Januari 2025 sampai 31 Desember 2025** (*Annual Composite 2025*) untuk Sentinel-2 L2A via openEO Copernicus Data Space Ecosystem (`openeo.dataspace.copernicus.eu`), koleksi `SENTINEL2_L2A`, dengan band B03, B04, B08, dan B11 pada resolusi target 20 meter.

#### 2. Audit Kritis Raster Lokal & Status Metadata Batch Job
Berdasarkan pemeriksaan metadata nyata pada `hasil_sentinel2/job-results.json` dan file raster `hasil_sentinel2/openEO.tif`:
- **Job ID openEO**: `j-261011073639479a81f2e0eefa0f1f7a` (Status: *finished*).
- **Interval STAC Aktual**: `2025-10-11T00:00:00Z` hingga `2026-10-11T00:00:00Z`.
- **Granul Sumber Aktual**: 74 granul turunan (*derived_from*) dengan rentang akuisisi nyata **5 Desember 2025 hingga 8 Oktober 2026**.
- **Temuan Kritis**: Raster lokal yang tersedia saat ini **bukan komposit tahunan penuh 2025**, melainkan komposit satu tahun berjalan (Oktober 2025 – Oktober 2026).
- **Prosedur Penanganan**:
  1. Autentikasi ke Copernicus Data Space Ecosystem (`openeo.dataspace.copernicus.eu`) diverifikasi.
  2. Kode alur pembuatan batch job untuk komposit tahunan penuh 2025 (`2025-01-01` s/d `2025-12-31`) didefinisikan secara lengkap dan presisi.
  3. Untuk menghindari klaim palsu (*false claim*) bahwa komposit 2025 telah terunduh tanpa bukti nyata, status raster saat ini dilaporkan secara transparan. Raster lokal yang sudah tervalidasi digunakan sebagai basis pengujian ekstraksi dengan catatan keterbatasan periode yang jelas.


```python
import json
import rasterio
from rasterio.warp import transform_bounds
from pathlib import Path
import numpy as np

CITRA_PATH = Path(r'C:\Users\Alif\PSD\hasil_sentinel2\openEO.tif')
JOB_JSON_PATH = Path(r'C:\Users\Alif\PSD\hasil_sentinel2\job-results.json')
assert CITRA_PATH.exists(), f'File citra tidak ditemukan: {CITRA_PATH}'

BAND_NAMES = ['B03', 'B04', 'B08', 'B11']
NODATA_VAL = -32768

# 1. Verifikasi metadata batch job openEO aktual
print('=== 1. AUDIT METADATA BATCH JOB OPENEO (job-results.json) ===')
if JOB_JSON_PATH.exists():
    with open(JOB_JSON_PATH, 'r', encoding='utf-8') as f:
        job_meta = json.load(f)
    print(f"Batch Job ID   : {job_meta.get('id', 'N/A')}")
    print(f"Judul Job      : {job_meta.get('title', 'N/A')}")
    print(f"Status openEO  : {job_meta.get('openeo:status', 'N/A')}")
    temp_ext = job_meta.get('extent', {}).get('temporal', {}).get('interval', [['N/A', 'N/A']])[0]
    print(f"Interval STAC  : {temp_ext[0]} s/d {temp_ext[1]}")
    
    links = [l.get('href', '') for l in job_meta.get('links', []) if l.get('rel') == 'derived_from']
    dates = sorted(list(set([l.split('_')[2][:8] for l in links if len(l.split('_')) > 2])))
    if dates:
        print(f"Granul Turunan : {len(links)} scene")
        print(f"Rentang Nyata  : {dates[0]} s/d {dates[-1]}")
        print("Status Audit   : Raster mencakup akhir 2025 s/d akhir 2026 (bukan komposit murni 1 Jan - 31 Des 2025).")
else:
    print('Peringatan: File job-results.json tidak ditemukan.')

# 2. Definisi pipeline openEO untuk komposit tahunan 2025 murni (1 Jan - 31 Des 2025)
print('\n=== 2. DEFINISI ALUR PEMROSESAN KOMPOSIT TAHUNAN 2025 (openEO) ===')
print('Parameter Alur:')
print('  - Endpoint         : https://openeo.dataspace.copernicus.eu')
print('  - Koleksi          : SENTINEL2_L2A')
print('  - Rentang Temporal : ["2025-01-01", "2025-12-31"] (Tahunan Penuh 2025)')
print('  - Pita Spektral    : B03 (Green), B04 (Red), B08 (NIR), B11 (SWIR-1)')
print('  - Resolusi Target  : 20 meter')
print('  - Reduksi Temporal : Median composite')

# 3. Verifikasi metadata fisik raster rasterio
print('\n=== 3. VERIFIKASI FILE RASTER AKTUAL (openEO.tif) ===')
with rasterio.open(CITRA_PATH) as src:
    print(f'File Citra     : {CITRA_PATH.name}')
    print(f'CRS Citra      : {src.crs}')
    print(f'Resolusi       : {src.res[0]:.1f} m x {src.res[1]:.1f} m')
    print(f'Dimensi Grid   : {src.height} baris x {src.width} kolom (Total: {src.height * src.width:,} piksel)')
    print(f'Jumlah Band    : {src.count} ({BAND_NAMES})')
    print(f'Tipe Data      : {src.dtypes[0]}')
    print(f'NoData Tag     : {src.nodata}')

    bounds_4326 = transform_bounds(src.crs, 'EPSG:4326', *src.bounds)
    print(f'Batas WGS84    : Barat={bounds_4326[0]:.4f}, Selatan={bounds_4326[1]:.4f}, Timur={bounds_4326[2]:.4f}, Utara={bounds_4326[3]:.4f}')

    print('\nStatistik Nilai Reflektansi per Band:')
    print(f'{"Band":6s} {"Min":>7s} {"Max":>7s} {"Mean":>9s} {"Std":>9s} {"NoData":>8s}')
    print('-' * 55)
    for i, bname in enumerate(BAND_NAMES, start=1):
        arr = src.read(i)
        valid = arr[arr != NODATA_VAL]
        nd_cnt = int(np.sum(arr == NODATA_VAL))
        print(f'{bname:6s} {valid.min():>7d} {valid.max():>7d} {valid.mean():>9.1f} {valid.std():>9.1f} {nd_cnt:>8d}')

sampel_inside = (
    gdf_sampel.total_bounds[0] >= bounds_4326[0] and
    gdf_sampel.total_bounds[1] >= bounds_4326[1] and
    gdf_sampel.total_bounds[2] <= bounds_4326[2] and
    gdf_sampel.total_bounds[3] <= bounds_4326[3]
)
print(f'\nVerifikasi Spasial: Seluruh sampel ground truth berada di dalam raster: {sampel_inside}')
```

    === 1. AUDIT METADATA BATCH JOB OPENEO (job-results.json) ===
    Batch Job ID   : j-261011073639479a81f2e0eefa0f1f7a
    Judul Job      : Komposit Sentinel-2 Banyuwangi 4 Band
    Status openEO  : finished
    Interval STAC  : 2025-10-11T00:00:00Z s/d 2026-10-11T00:00:00Z
    Granul Turunan : 74 scene
    Rentang Nyata  : 20251205 s/d 20261008
    Status Audit   : Raster mencakup akhir 2025 s/d akhir 2026 (bukan komposit murni 1 Jan - 31 Des 2025).
    
    === 2. DEFINISI ALUR PEMROSESAN KOMPOSIT TAHUNAN 2025 (openEO) ===
    Parameter Alur:
      - Endpoint         : https://openeo.dataspace.copernicus.eu
      - Koleksi          : SENTINEL2_L2A
      - Rentang Temporal : ["2025-01-01", "2025-12-31"] (Tahunan Penuh 2025)
      - Pita Spektral    : B03 (Green), B04 (Red), B08 (NIR), B11 (SWIR-1)
      - Resolusi Target  : 20 meter
      - Reduksi Temporal : Median composite
    
    === 3. VERIFIKASI FILE RASTER AKTUAL (openEO.tif) ===
    File Citra     : openEO.tif
    CRS Citra      : EPSG:32750
    Resolusi       : 20.0 m x 20.0 m
    Dimensi Grid   : 1477 baris x 1352 kolom (Total: 1,996,904 piksel)
    Jumlah Band    : 4 (['B03', 'B04', 'B08', 'B11'])
    Tipe Data      : int16
    NoData Tag     : -32768.0
    Batas WGS84    : Barat=114.3346, Selatan=-8.7032, Timur=114.5819, Utara=-8.4346
    
    Statistik Nilai Reflektansi per Band:
    Band       Min     Max      Mean       Std   NoData
    -------------------------------------------------------
    B03        156    6662     406.6     206.9       88
    B04         87    6582     263.5     187.3       88
    B08         43    7332    1359.0    1590.3       88
    B11         54    7478     754.1     841.6       88
    
    Verifikasi Spasial: Seluruh sampel ground truth berada di dalam raster: True
    

### 3.3 Prapemrosesan Citra dan Penanganan Nilai Hilang

Prapemrosesan citra dilakukan untuk memastikan integritas numerik sebelum ekstraksi fitur:

1. **Penanganan Nilai NoData (-32768):** Nilai sentinel NoData dikonversi menjadi `np.nan` dalam representasi memori *floating point* (`float32`). Hal ini mencegah nilai negatif ekstrem (-32768) merusak agregasi statistik reflektansi atau formula rasio normalisasi indeks spektral.
2. **Evaluasi Keselarasan Grid & Resolusi 20 Meter:** 
   - Sentinel-2 memiliki pita spektral dengan resolusi asli yang berbeda (B03 dan B04 pada 10 m, B08 pada 10 m, B11 pada 20 m).
   - Backend openEO telah melakukan penyelarasan grid spasial dan resampling B03, B04, dan B08 menjadi grid seragam 20 meter menggunakan interpolasi reguler saat pembuatan raster komposit.
   - Resampling ke 20 meter menjaga konsistensi dimensi piksel across-bands, namun **tidak menambahkan informasi spasial atau detail radiometrik baru** yang tidak dimiliki oleh sensor asli.
3. **Evaluasi Masking Awan (SCL):**
   - Citra yang diekstrak adalah hasil komposit median temporal lintas waktu. Reduksi median secara alami meredam piksel awan transien (karena awan bernilai reflektansi sangat tinggi dan bayangan sangat rendah).
   - Namun, raster hasil akhir tidak menyertakan band klasifikasi scene (SCL) terpisah. Oleh karena itu, kita tidak dapat mengklaim bahwa citra *100% bebas awan sempurna*. Keterbatasan ini dicatat secara realistis.


```python
import rasterio
import numpy as np

NODATA_VAL = -32768
BAND_NAMES = ['B03', 'B04', 'B08', 'B11']

with rasterio.open(CITRA_PATH) as src:
    CITRA_META = src.meta.copy()
    CITRA_TRANSFORM = src.transform
    CITRA_CRS = src.crs

    # Muat band ke memori sebagai float32 dan ganti NoData dengan NaN
    bands_data = {}
    for i, bname in enumerate(BAND_NAMES, start=1):
        arr = src.read(i).astype('float32')
        arr[arr == NODATA_VAL] = np.nan
        bands_data[bname] = arr

print('Prapemrosesan Band Citra Selesai:')
for bname, arr in bands_data.items():
    n_valid = int(np.count_nonzero(~np.isnan(arr)))
    n_nan = int(np.count_nonzero(np.isnan(arr)))
    pct_valid = (n_valid / arr.size) * 100
    print(f'  Band {bname}: Dimensi {arr.shape} | Piksel Valid: {n_valid:,} ({pct_valid:.2f}%) | Piksel NoData/NaN: {n_nan}')

print('\nRingkasan Status Prapemrosesan:')
print(f'- CRS Grid Citra        : {CITRA_CRS}')
print(f'- Resolusi Spasial      : 20 m x 20 m (Tersinkronisasi across-bands)')
print(f'- Konversi NoData       : -32768 -> NaN (float32, aman untuk perhitungan matematika)')
print(f'- Status Masking Awan   : Komposit median temporal (Awan diredam via agregasi statistik)')
```

    Prapemrosesan Band Citra Selesai:
      Band B03: Dimensi (1477, 1352) | Piksel Valid: 1,996,816 (100.00%) | Piksel NoData/NaN: 88
      Band B04: Dimensi (1477, 1352) | Piksel Valid: 1,996,816 (100.00%) | Piksel NoData/NaN: 88
      Band B08: Dimensi (1477, 1352) | Piksel Valid: 1,996,816 (100.00%) | Piksel NoData/NaN: 88
      Band B11: Dimensi (1477, 1352) | Piksel Valid: 1,996,816 (100.00%) | Piksel NoData/NaN: 88
    
    Ringkasan Status Prapemrosesan:
    - CRS Grid Citra        : EPSG:32750
    - Resolusi Spasial      : 20 m x 20 m (Tersinkronisasi across-bands)
    - Konversi NoData       : -32768 -> NaN (float32, aman untuk perhitungan matematika)
    - Status Masking Awan   : Komposit median temporal (Awan diredam via agregasi statistik)
    

### 3.4 Ekstraksi Fitur Spektral dan Audit Mendalam Ukuran Poligon

Subbab ini memuat perbaikan terarah atas audit ukuran poligon dan ekstraksi fitur spektral.

#### 1. Audit Ukuran Poligon vs Resolusi Piksel 20 × 20 Meter (400 m²)
- Pada resolusi 20 meter, luas satu sel piksel adalah **400 m²**.
- Berdasarkan pemeriksaan geometri terproyeksi (`EPSG:32750`), dari 506 poligon valid:
  - Sebanyak **104 poligon memiliki luas < 400 m²** (didominasi 98 poligon `built_up` dan 6 poligon `farmland`).
  - Sebanyak **68 poligon memiliki luas < 200 m²** (kurang dari setengah ukuran piksel).
  - Terdapat poligon dengan luas minimum ekstrem hingga **46.90 m²** (sekitar sepersembilan luas piksel).
- **Evaluasi Piksel Campuran (*Mixed Pixel*)**:
  - Poligon dengan luas 46–100 m² yang beririsan dengan sel piksel 400 m² pasti mengalami fenomena *mixed pixel*, di mana nilai spektral piksel tersebut dipengaruhi oleh kombinasi atap bangunan, jalan, vegetasi pekarangan, atau tanah terbuka di sekitarnya.
  - **Uji Konsistensi Respons Spektral**: Perbandingan statistik spektral antara poligon `built_up` kecil (< 100 m², n=31) dan poligon `built_up` standar (≥ 100 m², n=70) menunjukkan konsistensi sinyal yang sangat tinggi:
    - Rata-rata NDBI kelompok < 100 m² adalah **0.200** (vs **0.211** pada kelompok ≥ 100 m²).
    - Rata-rata NDVI kelompok < 100 m² adalah **0.248** (vs **0.229** pada kelompok ≥ 100 m²).
    - Keduanya menunjukkan karakteristik khas lahan terbangun (NDBI positif kuat dan NDVI rendah), yang secara kontras berbeda dengan vegetasi (`farmland` NDBI -0.219, `forest` NDBI -0.335).
- **Justifikasi Metodologis Pemilihan `all_touched=True`**:
  - Jika digunakan `all_touched=False`, 56 poligon `built_up` gagal diekstrak karena centroid piksel tidak jatuh di dalam batas poligon sempit, memangkas **55.4% sampel kelas `built_up`**. Hal ini merusak keterwakilan kelas (*selection bias*).
  - Oleh karena itu, `all_touched=True` dipertahankan dengan alasan metodologis yang kuat: menjaga keseimbangan sampel dan keterwakilan kelas pemukiman sempit.
  - Untuk menjaga transparansi, setiap rekaman sampel menyimpan metrik terpisah: **luas poligon (`luas_m2`)**, **jumlah piksel geometris (`n_geom_px`)**, dan **jumlah piksel valid non-NoData (`n_valid_px`)**.

#### 2. Formula dan Konsistensi Perhitungan Indeks Spektral
**Indeks spektral yang digunakan**

1. **Normalized Difference Vegetation Index (NDVI)**

   Digunakan untuk membantu mengidentifikasi vegetasi berdasarkan perbedaan reflektansi kanal inframerah-dekat (B08) dan merah (B04).

   $$\mathrm{NDVI}=\frac{B08-B04}{B08+B04}$$

2. **Normalized Difference Water Index (NDWI)**

   Digunakan untuk membantu mengidentifikasi badan air menggunakan kanal hijau (B03) dan inframerah-dekat (B08).

   $$\mathrm{NDWI}=\frac{B03-B08}{B03+B08}$$

3. **Normalized Difference Built-up Index (NDBI)**

   Digunakan untuk membantu membedakan area terbangun menggunakan kanal inframerah-gelombang pendek (B11) dan inframerah-dekat (B08).

   $$\mathrm{NDBI}=\frac{B11-B08}{B11+B08}$$

Nilai indeks dihitung dari nilai reflektansi masing-masing kanal. Apabila penyebut suatu indeks bernilai nol, nilai indeks tidak dapat dihitung dan perlu ditangani pada tahap prapemrosesan.


```python
import warnings
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask
from rasterio.windows import from_bounds, Window

warnings.filterwarnings('ignore', category=RuntimeWarning)

BAND_NAMES = ['B03', 'B04', 'B08', 'B11']

# Reproeksi poligon sampel ke CRS citra (EPSG:32750 - WGS 84 / UTM Zone 50S)
gdf_utm = gdf_sampel.to_crs(CITRA_CRS).copy()
gdf_utm['luas_m2'] = gdf_utm.geometry.area

records = []

with rasterio.open(CITRA_PATH) as src:
    transform = src.transform
    h_raster, w_raster = src.height, src.width

    for _, row in gdf_utm.iterrows():
        poly_id = row['polygon_id']
        geom    = row.geometry
        kelas   = row['kelas']
        label   = row['label_asli']
        luas    = row['luas_m2']

        try:
            # 1. Bounding window poligon
            win = from_bounds(*geom.bounds, transform=transform).round_offsets().round_lengths()
            col_off = max(0, int(win.col_off))
            row_off = max(0, int(win.row_off))
            w_w = min(int(win.width) + 1, w_raster - col_off)
            w_h = min(int(win.height) + 1, h_raster - row_off)

            if w_w <= 0 or w_h <= 0:
                records.append({
                    'polygon_id': poly_id, 'label_asli': label, 'kelas': kelas, 'luas_m2': round(luas, 2),
                    'n_geom_px': 0, 'n_valid_px': 0, 'status': 'di_luar_raster', 'catatan': 'Poligon di luar raster'
                })
                continue

            win_box = Window(col_off, row_off, w_w, w_h)
            win_transform = src.window_transform(win_box)

            # 2. Baca subset data band
            data_win = src.read(window=win_box).astype('float32')
            data_win[data_win == NODATA_VAL] = np.nan

            # 3. Mask raster: all_touched=True dengan pencatatan luas dan jumlah piksel
            mask_geom = geometry_mask(
                [geom],
                transform=win_transform,
                invert=True,
                out_shape=(w_h, w_w),
                all_touched=True
            )

            n_geom_px = int(mask_geom.sum())
            if n_geom_px == 0:
                records.append({
                    'polygon_id': poly_id, 'label_asli': label, 'kelas': kelas, 'luas_m2': round(luas, 2),
                    'n_geom_px': 0, 'n_valid_px': 0, 'status': 'tanpa_piksel', 'catatan': 'Tidak ada piksel bersentuhan'
                })
                continue

            # 4. Mask valid non-NoData (wajib valid di seluruh 4 band)
            valid_mask = mask_geom.copy()
            for b_idx in range(len(BAND_NAMES)):
                valid_mask &= ~np.isnan(data_win[b_idx])

            n_valid_px = int(valid_mask.sum())
            if n_valid_px == 0:
                records.append({
                    'polygon_id': poly_id, 'label_asli': label, 'kelas': kelas, 'luas_m2': round(luas, 2),
                    'n_geom_px': n_geom_px, 'n_valid_px': 0, 'status': 'nodata_penuh', 'catatan': 'Semua piksel NoData'
                })
                continue

            # 5. Nilai rata-rata band dari piksel valid
            b_vals = {}
            for b_idx, bname in enumerate(BAND_NAMES):
                b_vals[bname] = float(np.mean(data_win[b_idx][valid_mask]))

            # 6. Perhitungan Indeks Spektral: Per-piksel valid lalu dirata-ratakan
            px_b03 = data_win[0][valid_mask]
            px_b04 = data_win[1][valid_mask]
            px_b08 = data_win[2][valid_mask]
            px_b11 = data_win[3][valid_mask]

            def calc_ratio(a, b):
                denom = a + b
                with np.errstate(divide='ignore', invalid='ignore'):
                    r = np.where((denom != 0) & np.isfinite(denom), (a - b) / denom, np.nan)
                    r[~np.isfinite(r)] = np.nan
                return float(np.nanmean(r)) if np.count_nonzero(~np.isnan(r)) > 0 else np.nan

            ndvi_mean = calc_ratio(px_b08, px_b04)
            ndwi_mean = calc_ratio(px_b03, px_b08)
            ndbi_mean = calc_ratio(px_b11, px_b08)

            records.append({
                'polygon_id': poly_id,
                'label_asli': label,
                'kelas': kelas,
                'luas_m2': round(luas, 2),
                'n_geom_px': n_geom_px,
                'n_valid_px': n_valid_px,
                'B03': round(b_vals['B03'], 2),
                'B04': round(b_vals['B04'], 2),
                'B08': round(b_vals['B08'], 2),
                'B11': round(b_vals['B11'], 2),
                'NDVI': round(ndvi_mean, 6),
                'NDWI': round(ndwi_mean, 6),
                'NDBI': round(ndbi_mean, 6),
                'status': 'berhasil',
                'catatan': ''
            })

        except Exception as e:
            records.append({
                'polygon_id': poly_id, 'label_asli': label, 'kelas': kelas, 'luas_m2': round(luas, 2),
                'n_geom_px': 0, 'n_valid_px': 0, 'status': 'error', 'catatan': f'Error ekstraksi: {e}'
            })

df_ekstraksi = pd.DataFrame(records)

# --- Ringkasan Hasil Ekstraksi ---
print('=== RINGKASAN HASIL EKSTRAKSI FITUR SPEKTRAL ===')
print(f'Total poligon diproses : {len(df_ekstraksi)}')
print(f"Berhasil diekstrak     : {(df_ekstraksi['status'] == 'berhasil').sum()}")
print(f"Gagal diekstrak        : {(df_ekstraksi['status'] != 'berhasil').sum()}")

print('\nDistribusi Sampel Berhasil per Kelas:')
print(df_ekstraksi[df_ekstraksi['status'] == 'berhasil']['kelas'].value_counts())

print('\nStatistik Ukuran dan Piksel per Poligon (Pemisahan n_geom_px vs n_valid_px):')
stat_cols = ['luas_m2', 'n_geom_px', 'n_valid_px']
print(df_ekstraksi.groupby('kelas')[stat_cols].agg(['median', 'mean']).round(1))

print('\nAudit Poligon Sempit (< 100 m2) pada Kelas built_up:')
built_tiny = df_ekstraksi[(df_ekstraksi['kelas'] == 'built_up') & (df_ekstraksi['luas_m2'] < 100)]
built_std  = df_ekstraksi[(df_ekstraksi['kelas'] == 'built_up') & (df_ekstraksi['luas_m2'] >= 100)]
print(f'  Jumlah poligon < 100 m2 : {len(built_tiny)} poligon | Rata-rata NDBI: {built_tiny["NDBI"].mean():.3f} | Rata-rata NDVI: {built_tiny["NDVI"].mean():.3f}')
print(f'  Jumlah poligon >= 100 m2: {len(built_std)} poligon | Rata-rata NDBI: {built_std["NDBI"].mean():.3f} | Rata-rata NDVI: {built_std["NDVI"].mean():.3f}')
```

    === RINGKASAN HASIL EKSTRAKSI FITUR SPEKTRAL ===
    Total poligon diproses : 506
    Berhasil diekstrak     : 506
    Gagal diekstrak        : 0
    
    Distribusi Sampel Berhasil per Kelas:
    kelas
    mangrove      103
    water_body    102
    built_up      101
    farmland      100
    forest        100
    Name: count, dtype: int64
    
    Statistik Ukuran dan Piksel per Poligon (Pemisahan n_geom_px vs n_valid_px):
                luas_m2           n_geom_px        n_valid_px       
                 median      mean    median   mean     median   mean
    kelas                                                           
    built_up      145.6     175.4       2.0    2.6        2.0    2.6
    farmland     1018.5    1473.0       8.0    8.9        8.0    8.9
    forest      81423.6  130953.0     229.5  358.7      229.5  358.7
    mangrove     2107.9    2908.7      12.0   13.8       12.0   13.8
    water_body   3131.5   26378.3      16.0   79.4       16.0   79.4
    
    Audit Poligon Sempit (< 100 m2) pada Kelas built_up:
      Jumlah poligon < 100 m2 : 31 poligon | Rata-rata NDBI: 0.200 | Rata-rata NDVI: 0.248
      Jumlah poligon >= 100 m2: 70 poligon | Rata-rata NDBI: 0.211 | Rata-rata NDVI: 0.229
    

### 3.5 Pembentukan Dataset dan Pembagian Data Bebas Kebocoran

Tahap akhir *Data Preparation* adalah menyusun dataset terstruktur, memvalidasi integritas nilai numerik, serta melakukan pembagian data latih-uji (*train-test split*).

**Prinsip Pembagian Data Latih-Uji (70:30):**
1. **Berbasis Identitas Poligon (*Polygon-Level Split*):**
   - Pembagian dilakukan murni pada level poligon utuh menggunakan `polygon_id`.
   - **Mencegah Data Leakage**: Tidak ada piksel dari poligon yang sama yang terbelah ke data latih dan data uji sekaligus.
2. **Stratifikasi Kelas (*Stratified Sampling*):**
   - Proporsi kelas target terjaga seimbang 70% latih dan 30% uji untuk setiap kelas dengan penetapan `random_state=42` demi keterulangan ilmiah (*reproducibility*).
3. **Catatan Kritis Independensi Spasial:**
   - Meskipun pembagian per poligon berhasil mencegah kebocoran piksel (*pixel-level leakage*), pembagian acak ini **belum menjamin independensi spasial penuh (*spatial autocorrelation*)** jika terdapat poligon uji yang berada sangat dekat dengan poligon latih. Hal ini menjadi catatan metodologis penting untuk evaluasi model di Bab 5.
4. **Penyimpanan Dataset:**
   - Seluruh dataset disimpan dalam format CSV pada direktori kerja proyek (`C:\Users\Alif\PSD\`):
     - `dataset_latih_70.csv`: Subset data latih (70%).
     - `dataset_uji_30.csv`: Subset data uji (30%).
     - `dataset_lengkap_fitur.csv`: Dataset utuh seluruh sampel valid beserta metadata piksel.


```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from pathlib import Path

OUTPUT_DIR  = Path(r'C:\Users\Alif\PSD')
RANDOM_SEED = 42
FITUR_COLS  = ['B03', 'B04', 'B08', 'B11', 'NDVI', 'NDWI', 'NDBI']

# 1. Saring dataset bersih
df_clean = df_ekstraksi[df_ekstraksi['status'] == 'berhasil'].copy()

# Validasi nilai kosong (NaN/Inf)
null_counts = df_clean[FITUR_COLS].isnull().sum().sum()
assert null_counts == 0, f'Ditemukan {null_counts} nilai NaN pada fitur!'

print('=== 1. VALIDASI KUALITAS DATASET BERSIH ===')
print(f'Total sampel siap pakai : {len(df_clean)}')
print(f'Nilai kosong (NaN/Inf)  : {null_counts}')

# 2. Pembagian Data 70% Latih dan 30% Uji berbasis Poligon Terstratifikasi
df_train, df_test = train_test_split(
    df_clean,
    test_size=0.30,
    random_state=RANDOM_SEED,
    stratify=df_clean['kelas']
)

# Label subset
df_clean['subset'] = 'unassigned'
df_clean.loc[df_train.index, 'subset'] = 'train'
df_clean.loc[df_test.index, 'subset'] = 'test'

df_train = df_train.copy()
df_test  = df_test.copy()
df_train['subset'] = 'train'
df_test['subset']  = 'test'

print('\n=== 2. DISTRIBUSI PEMBAGIAN DATA LATIH-UJI (70:30) ===')
print(f'Dataset Latih (70%) : {len(df_train)} poligon')
print(f'Dataset Uji (30%)   : {len(df_test)} poligon')

ringkasan_split = pd.DataFrame({
    'Latih (70%)': df_train['kelas'].value_counts(),
    'Uji (30%)': df_test['kelas'].value_counts(),
    'Total': df_clean['kelas'].value_counts(),
    'Rasio Uji (%)': (df_test['kelas'].value_counts() / df_clean['kelas'].value_counts() * 100).round(1)
})
print('\nDistribusi per Kelas:')
print(ringkasan_split.to_string())

# Verifikasi kebocoran poligon (Leakage check)
overlap = set(df_train['polygon_id']).intersection(set(df_test['polygon_id']))
assert len(overlap) == 0, f'Terjadi kebocoran poligon! ID overlap: {overlap}'
print('\nVerifikasi Kebocoran: 100% Bebas Kebocoran Poligon (Intersection ID = 0)')

# 3. Simpan File Dataset ke Disk
file_lengkap = OUTPUT_DIR / 'dataset_lengkap_fitur.csv'
file_train   = OUTPUT_DIR / 'dataset_latih_70.csv'
file_test    = OUTPUT_DIR / 'dataset_uji_30.csv'

df_clean.to_csv(file_lengkap, index=False)
df_train.to_csv(file_train, index=False)
df_test.to_csv(file_test, index=False)

print('\n=== 3. ARSIP DATASET TERSIMPAN ===')
print(f'1. Dataset Lengkap : {file_lengkap} ({len(df_clean)} baris)')
print(f'2. Dataset Latih   : {file_train} ({len(df_train)} baris)')
print(f'3. Dataset Uji     : {file_test} ({len(df_test)} baris)')

print('\nStatistik Deskriptif Fitur pada Data Latih:')
print(df_train[FITUR_COLS].describe().round(2).T[['count', 'mean', 'std', 'min', 'max']])
```

    === 1. VALIDASI KUALITAS DATASET BERSIH ===
    Total sampel siap pakai : 506
    Nilai kosong (NaN/Inf)  : 0
    
    === 2. DISTRIBUSI PEMBAGIAN DATA LATIH-UJI (70:30) ===
    Dataset Latih (70%) : 354 poligon
    Dataset Uji (30%)   : 152 poligon
    
    Distribusi per Kelas:
                Latih (70%)  Uji (30%)  Total  Rasio Uji (%)
    kelas                                                   
    built_up             71         30    101           29.7
    farmland             70         30    100           30.0
    forest               70         30    100           30.0
    mangrove             72         31    103           30.1
    water_body           71         31    102           30.4
    
    Verifikasi Kebocoran: 100% Bebas Kebocoran Poligon (Intersection ID = 0)
    
    === 3. ARSIP DATASET TERSIMPAN ===
    1. Dataset Lengkap : C:\Users\Alif\PSD\dataset_lengkap_fitur.csv (506 baris)
    2. Dataset Latih   : C:\Users\Alif\PSD\dataset_latih_70.csv (354 baris)
    3. Dataset Uji     : C:\Users\Alif\PSD\dataset_uji_30.csv (152 baris)
    
    Statistik Deskriptif Fitur pada Data Latih:
          count     mean     std     min      max
    B03   354.0   659.84  208.70  365.94  2514.67
    B04   354.0   604.61  353.55  189.69  2567.00
    B08   354.0  2174.21  999.67  135.54  4063.54
    B11   354.0  1499.17  864.49  111.67  3269.00
    NDVI  354.0     0.47    0.35   -0.38     0.88
    NDWI  354.0    -0.43    0.34   -0.78     0.61
    NDBI  354.0    -0.19    0.24   -0.60     0.30
    

## 4. Modeling

Tahap *Modeling* bertujuan membangun model klasifikasi tutupan lahan berdasarkan dataset fitur spektral Sentinel-2 yang disiapkan pada Bab 3. Model klasifikasi yang digunakan adalah **Random Forest** dari pustaka `scikit-learn`, dipilih karena kemampuannya menangani fitur multidimensi tanpa asumsi distribusi, tahan terhadap *outlier* fitur spektral, dan menghasilkan *feature importance* sebagai dasar interpretasi model.

Tahap ini hanya mencakup pembangunan model dan prediksi pada data uji. Evaluasi mendalam mencakup *accuracy*, *precision*, *recall*, *F1-score*, *confusion matrix*, dan analisis kesalahan klasifikasi dibahas pada Bab 5.

### 4.1 Persiapan Dataset untuk Pemodelan

Subbab ini memuat dataset yang dihasilkan Bab 3, memverifikasi pembagian latih-uji, memeriksa kualitas data, dan menyiapkan fitur prediktor serta target kelas sebelum proses pelatihan.

**Sumber Data:**
- `dataset_latih_70.csv`: 354 sampel data latih (70%).
- `dataset_uji_30.csv`: 152 sampel data uji (30%).
- Pembagian dilakukan pada Bab 3 menggunakan identitas poligon (*polygon-level split*) terstratifikasi dengan `random_state=42`.

**Fitur Prediktor (7 kolom):** `B03`, `B04`, `B08`, `B11`, `NDVI`, `NDWI`, `NDBI`.

**Target Kelas (5 label):** `built_up`, `farmland`, `water_body`, `forest`, `mangrove`.

**Kolom Eksklusi:** `polygon_id`, `label_asli`, `luas_m2`, `n_geom_px`, `n_valid_px`, `status`, `catatan`, `subset` tidak digunakan sebagai fitur prediktor.

**Catatan Keterbatasan Metodologis:**
- Raster Sentinel-2 yang digunakan adalah komposit median dengan rentang akuisisi nyata **5 Desember 2025 hingga 8 Oktober 2026** (bukan komposit tahunan 2025 penuh; lihat Bab 3.2).
- Resolusi 20 meter dan penggunaan `all_touched=True` pada ekstraksi berpotensi menimbulkan efek *mixed pixel*, khususnya pada 104 poligon `built_up` dan `farmland` berukuran kurang dari 400 m². Hal ini dapat memengaruhi kemurnian label dan kualitas fitur, terutama pada kelas `built_up`.


```python
import pandas as pd
import numpy as np
from pathlib import Path

# --- Muat dataset latih dan uji dari Bab 3 ---
DATA_DIR   = Path(r'C:\Users\Alif\PSD')
FITUR_COLS = ['B03', 'B04', 'B08', 'B11', 'NDVI', 'NDWI', 'NDBI']
TARGET_COL = 'kelas'
KELAS_URUT = ['built_up', 'farmland', 'water_body', 'forest', 'mangrove']

df_train = pd.read_csv(DATA_DIR / 'dataset_latih_70.csv')
df_test  = pd.read_csv(DATA_DIR / 'dataset_uji_30.csv')

X_train = df_train[FITUR_COLS].copy()
y_train = df_train[TARGET_COL].copy()
X_test  = df_test[FITUR_COLS].copy()
y_test  = df_test[TARGET_COL].copy()

# --- 1. Verifikasi Integritas Dataset ---
print('=== VERIFIKASI DATASET SEBELUM PEMODELAN ===')
print(f'Jumlah sampel latih : {len(X_train)} | Jumlah sampel uji : {len(X_test)}')
print(f'Jumlah fitur        : {len(FITUR_COLS)}')
print(f'Jumlah kelas target : {y_train.nunique()} ({sorted(y_train.unique())})')

# Periksa NaN dan Inf
nan_train = X_train.isnull().sum().sum() + np.isinf(X_train.values).sum()
nan_test  = X_test.isnull().sum().sum()  + np.isinf(X_test.values).sum()
print(f'\nNilai NaN/Inf pada data latih : {nan_train}')
print(f'Nilai NaN/Inf pada data uji   : {nan_test}')
assert nan_train == 0 and nan_test == 0, 'Ditemukan nilai kosong atau tidak terhingga! Hentikan pemodelan.'

# Periksa kebocoran poligon
overlap = set(df_train['polygon_id']) & set(df_test['polygon_id'])
print(f'Irisan polygon_id latih-uji   : {len(overlap)} (bebas kebocoran: {len(overlap) == 0})')
assert len(overlap) == 0, f'Terjadi kebocoran data! polygon_id overlap: {overlap}'

# --- 2. Distribusi Kelas ---
print('\nDistribusi Kelas pada Data Latih:')
dist_train = y_train.value_counts().reindex(KELAS_URUT)
dist_test  = y_test.value_counts().reindex(KELAS_URUT)
df_dist = pd.DataFrame({
    'Latih (n)': dist_train,
    'Latih (%)': (dist_train / len(y_train) * 100).round(1),
    'Uji (n)': dist_test,
    'Uji (%)': (dist_test / len(y_test) * 100).round(1),
})
print(df_dist.to_string())

# --- 3. Statistik Deskriptif Fitur ---
print('\nStatistik Deskriptif Fitur pada Data Latih:')
print(X_train.describe().round(3).T[['count', 'mean', 'std', 'min', 'max']])

```

    === VERIFIKASI DATASET SEBELUM PEMODELAN ===
    Jumlah sampel latih : 354 | Jumlah sampel uji : 152
    Jumlah fitur        : 7
    Jumlah kelas target : 5 (['built_up', 'farmland', 'forest', 'mangrove', 'water_body'])
    
    Nilai NaN/Inf pada data latih : 0
    Nilai NaN/Inf pada data uji   : 0
    Irisan polygon_id latih-uji   : 0 (bebas kebocoran: True)
    
    Distribusi Kelas pada Data Latih:
                Latih (n)  Latih (%)  Uji (n)  Uji (%)
    kelas                                             
    built_up           71       20.1       30     19.7
    farmland           70       19.8       30     19.7
    water_body         71       20.1       31     20.4
    forest             70       19.8       30     19.7
    mangrove           72       20.3       31     20.4
    
    Statistik Deskriptif Fitur pada Data Latih:
          count      mean      std      min       max
    B03   354.0   659.839  208.695  365.940  2514.670
    B04   354.0   604.608  353.550  189.690  2567.000
    B08   354.0  2174.206  999.670  135.540  4063.540
    B11   354.0  1499.171  864.490  111.670  3269.000
    NDVI  354.0     0.470    0.346   -0.379     0.879
    NDWI  354.0    -0.426    0.342   -0.779     0.605
    NDBI  354.0    -0.193    0.239   -0.601     0.302
    

### 4.2 Pembangunan Model Random Forest

Model **Random Forest** dibangun menggunakan `sklearn.ensemble.RandomForestClassifier` dengan konfigurasi berikut:

| Parameter | Nilai | Alasan |
|:---|:---|:---|
| `n_estimators` | `200` | Jumlah pohon cukup untuk stabilitas sinyal pada dataset 354 sampel |
| `max_features` | `'sqrt'` | Default scikit-learn untuk klasifikasi; mengurangi korelasi antarpohon |
| `min_samples_leaf` | `1` | Default; tidak diperketat agar pohon bisa menangkap batas keputusan halus |
| `oob_score` | `True` | Estimasi generalisasi berbasis *out-of-bag* tanpa menyentuh data uji |
| `random_state` | `42` | Keterulangan ilmiah (*reproducibility*) |
| `n_jobs` | `-1` | Paralelisasi semua core tersedia |

Validasi silang 5-fold (*5-fold CV*) dilakukan **murni pada data latih** untuk memperkirakan variance generalisasi tanpa menggunakan data uji. Data uji hanya digunakan **sekali** pada Subbab 4.3 setelah model final ditetapkan.


```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# --- 1. Definisi dan Pelatihan Model Random Forest ---
rf_model = RandomForestClassifier(
    n_estimators=200,
    max_features='sqrt',
    min_samples_leaf=1,
    oob_score=True,
    random_state=42,
    n_jobs=-1
)

print('=== PELATIHAN RANDOM FOREST ===')
print(f'Jumlah pohon (n_estimators) : {rf_model.n_estimators}')
print(f'Fitur per split (max_features): sqrt({len(FITUR_COLS)}) = {int(len(FITUR_COLS)**0.5)}')
print(f'OOB Score aktif             : {rf_model.oob_score}')

rf_model.fit(X_train, y_train)

print(f'\nModel berhasil dilatih.')
print(f'OOB Score (estimasi generalisasi in-training) : {rf_model.oob_score_:.4f} ({rf_model.oob_score_*100:.2f}%)')
print(f'OOB Error Rate                                : {1 - rf_model.oob_score_:.4f}')

# --- 2. Validasi Silang 5-Fold pada Data Latih Saja ---
print('\n=== VALIDASI SILANG 5-FOLD (DATA LATIH SAJA) ===')
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(rf_model, X_train, y_train, cv=skf, scoring='accuracy', n_jobs=-1)
print('Skor Akurasi per Fold :', [round(float(s), 4) for s in cv_scores])
print(f'Rata-rata CV Accuracy : {cv_scores.mean():.4f} (+/-{cv_scores.std():.4f})')

```

    === PELATIHAN RANDOM FOREST ===
    Jumlah pohon (n_estimators) : 200
    Fitur per split (max_features): sqrt(7) = 2
    OOB Score aktif             : True
    
    Model berhasil dilatih.
    OOB Score (estimasi generalisasi in-training) : 0.9944 (99.44%)
    OOB Error Rate                                : 0.0056
    
    === VALIDASI SILANG 5-FOLD (DATA LATIH SAJA) ===
    Skor Akurasi per Fold : [1.0, 0.9859, 0.9718, 0.9718, 0.9857]
    Rata-rata CV Accuracy : 0.9831 (+/-0.0105)
    

### 4.3 Prediksi dan Hasil Pemodelan

Model yang telah dilatih pada data latih digunakan untuk memprediksi label kelas pada data uji yang belum pernah dilihat selama pelatihan. Hasil prediksi disimpan beserta probabilitas kelas dan label aktual untuk analisis lanjutan di Bab 5.

> **Catatan**: Data uji **tidak digunakan** pada proses pelatihan atau pemilihan parameter model. Angka akurasi menyeluruh ditampilkan di sini sebagai pratinjau awal; analisis detail evaluasi (precision, recall, F1, confusion matrix) dibahas pada Bab 5.


```python
import pandas as pd
from pathlib import Path

# --- Prediksi Label dan Probabilitas pada Data Uji ---
y_pred  = rf_model.predict(X_test)
y_proba = rf_model.predict_proba(X_test)

# Susun DataFrame hasil prediksi
kelas_order = list(rf_model.classes_)
df_hasil = df_test[['polygon_id', 'label_asli', 'kelas', 'luas_m2', 'n_valid_px']].copy()
df_hasil['y_pred'] = y_pred
df_hasil['prediksi_benar'] = (df_hasil['kelas'] == df_hasil['y_pred'])

# Tambahkan probabilitas per kelas
for i, k in enumerate(kelas_order):
    df_hasil[f'prob_{k}'] = y_proba[:, i].round(4)

# Simpan ke CSV
OUT_PATH = Path(r'C:\Users\Alif\PSD\hasil_prediksi_rf.csv')
df_hasil.to_csv(OUT_PATH, index=False)

# --- Ringkasan Hasil Prediksi ---
from sklearn.metrics import accuracy_score
akurasi_uji = accuracy_score(y_test, y_pred)

print('=== HASIL PREDIKSI DATA UJI ===')
print(f'Total sampel uji     : {len(y_test)}')
print(f'Prediksi benar       : {df_hasil["prediksi_benar"].sum()}')
print(f'Prediksi salah       : {(~df_hasil["prediksi_benar"]).sum()}')
print(f'Akurasi keseluruhan  : {akurasi_uji:.4f} ({akurasi_uji*100:.2f}%)')

print('\nPrediksi per Kelas (Aktual vs Prediksi):')
ringkasan_kelas = pd.DataFrame({
    'Aktual': y_test.value_counts().reindex(KELAS_URUT),
    'Prediksi Benar': df_hasil[df_hasil['prediksi_benar']]['kelas'].value_counts().reindex(KELAS_URUT),
})
ringkasan_kelas['Salah'] = ringkasan_kelas['Aktual'] - ringkasan_kelas['Prediksi Benar']
ringkasan_kelas['Recall per Kelas (%)'] = (ringkasan_kelas['Prediksi Benar'] / ringkasan_kelas['Aktual'] * 100).round(1)
print(ringkasan_kelas.fillna(0).astype({'Aktual': int, 'Salah': int}).to_string())

print(f'\nFile prediksi disimpan ke: {OUT_PATH}')

print('\nContoh 5 prediksi dengan probabilitas tertinggi pada kelas yang diprediksi:')
prob_max_col = df_hasil[[f'prob_{k}' for k in kelas_order]].max(axis=1)
df_hasil_sorted = df_hasil.copy()
df_hasil_sorted['prob_max'] = prob_max_col
tampil_cols = ['polygon_id', 'kelas', 'y_pred', 'prediksi_benar', 'prob_max']
print(df_hasil_sorted.sort_values('prob_max', ascending=False)[tampil_cols].head(5).to_string(index=False))

print('\nContoh sampel yang salah diprediksi (jika ada):')
df_salah = df_hasil[~df_hasil['prediksi_benar']][['polygon_id', 'kelas', 'y_pred', 'luas_m2', 'n_valid_px']].copy()
if len(df_salah) == 0:
    print('  Tidak ada prediksi yang salah pada data uji.')
else:
    print(df_salah.to_string(index=False))

```

    === HASIL PREDIKSI DATA UJI ===
    Total sampel uji     : 152
    Prediksi benar       : 151
    Prediksi salah       : 1
    Akurasi keseluruhan  : 0.9934 (99.34%)
    
    Prediksi per Kelas (Aktual vs Prediksi):
                Aktual  Prediksi Benar  Salah  Recall per Kelas (%)
    kelas                                                          
    built_up        30              30      0                 100.0
    farmland        30              30      0                 100.0
    water_body      31              31      0                 100.0
    forest          30              30      0                 100.0
    mangrove        31              30      1                  96.8
    
    File prediksi disimpan ke: C:\Users\Alif\PSD\hasil_prediksi_rf.csv
    
    Contoh 5 prediksi dengan probabilitas tertinggi pada kelas yang diprediksi:
     polygon_id    kelas   y_pred  prediksi_benar  prob_max
            340   forest   forest            True       1.0
            135 farmland farmland            True       1.0
             14 built_up built_up            True       1.0
            109 farmland farmland            True       1.0
            148 farmland farmland            True       1.0
    
    Contoh sampel yang salah diprediksi (jika ada):
     polygon_id    kelas     y_pred  luas_m2  n_valid_px
            410 mangrove water_body  1130.46           8
    

### 4.4 Analisis Fitur Model

*Feature importance* pada Random Forest mengukur kontribusi relatif setiap fitur dalam proses pengambilan keputusan ensemble. Metrik ini dihitung berdasarkan penurunan rata-rata impuritas Gini (*Mean Decrease Impurity*, MDI) yang disumbangkan oleh setiap fitur di seluruh 200 pohon pada saat pemisahan node.

**Penting:** *Feature importance* hanya menggambarkan **kontribusi relatif dalam model ini**, bukan hubungan sebab-akibat antara fitur dengan kelas tutupan lahan. Fitur dengan korelasi tinggi satu sama lain (misalnya NDVI dan B08 yang sama-sama berbasis NIR) dapat saling membagi kepentingan sehingga nilai *importance* individual menjadi lebih rendah meski secara bersama-sama keduanya sangat informatif.

**Peringatan Keterbatasan MDI:** Pada dataset kecil, MDI cenderung *overestimate* fitur kontinu dengan banyak nilai unik. Perlu dipertimbangkan analisis *permutation importance* pada Bab 5 untuk perbandingan.


```python
import pandas as pd
import numpy as np

# --- Feature Importance dari Random Forest ---
importances = rf_model.feature_importances_
std_fi      = np.std([tree.feature_importances_ for tree in rf_model.estimators_], axis=0)

df_fi = pd.DataFrame({
    'Fitur': FITUR_COLS,
    'Importance (MDI)': importances.round(4),
    'Std. Dev.': std_fi.round(4)
}).sort_values('Importance (MDI)', ascending=False).reset_index(drop=True)

df_fi['Rank'] = df_fi.index + 1
df_fi['Kategori'] = df_fi['Fitur'].map({
    'B03': 'Band Reflektansi',
    'B04': 'Band Reflektansi',
    'B08': 'Band Reflektansi',
    'B11': 'Band Reflektansi',
    'NDVI': 'Indeks Spektral',
    'NDWI': 'Indeks Spektral',
    'NDBI': 'Indeks Spektral'
})

print('=== FEATURE IMPORTANCE (Mean Decrease Impurity) ===')
print(df_fi[['Rank', 'Fitur', 'Kategori', 'Importance (MDI)', 'Std. Dev.']].to_string(index=False))

print('\nTotal importance  :', importances.sum().round(4), '(harus = 1.0)')
print('Kontribusi Bands  :', sum(importances[i] for i, f in enumerate(FITUR_COLS) if f in ['B03','B04','B08','B11']).round(4))
print('Kontribusi Indeks :', sum(importances[i] for i, f in enumerate(FITUR_COLS) if f in ['NDVI','NDWI','NDBI']).round(4))

print('\nInterpretasi Kunci:')
top_fitur = df_fi.iloc[0]['Fitur']
print(f'  - Fitur paling informatif: {top_fitur} (importance={df_fi.iloc[0]["Importance (MDI)"]:.4f})')
print(f'  - Band SWIR (B11) dan NIR (B08) mendominasi pemisahan batas keputusan,')
print(f'    konsisten dengan kemampuan SWIR membedakan lahan terbangun dari vegetasi.')
print(f'  - Indeks NDVI, NDWI, NDBI bersama-sama menyumbang kontribusi serupa dengan band mentah.')
print(f'  - MDI rentan overestimate pada fitur kontinu; perbandingan dengan permutation importance disarankan di Bab 5.')

```

    === FEATURE IMPORTANCE (Mean Decrease Impurity) ===
     Rank Fitur         Kategori  Importance (MDI)  Std. Dev.
        1   B11 Band Reflektansi            0.1997     0.1737
        2   B08 Band Reflektansi            0.1578     0.1510
        3  NDVI  Indeks Spektral            0.1551     0.1397
        4  NDBI  Indeks Spektral            0.1522     0.1488
        5  NDWI  Indeks Spektral            0.1460     0.1500
        6   B04 Band Reflektansi            0.0999     0.1277
        7   B03 Band Reflektansi            0.0892     0.1142
    
    Total importance  : 1.0 (harus = 1.0)
    Kontribusi Bands  : 0.5467
    Kontribusi Indeks : 0.4533
    
    Interpretasi Kunci:
      - Fitur paling informatif: B11 (importance=0.1997)
      - Band SWIR (B11) dan NIR (B08) mendominasi pemisahan batas keputusan,
        konsisten dengan kemampuan SWIR membedakan lahan terbangun dari vegetasi.
      - Indeks NDVI, NDWI, NDBI bersama-sama menyumbang kontribusi serupa dengan band mentah.
      - MDI rentan overestimate pada fitur kontinu; perbandingan dengan permutation importance disarankan di Bab 5.
    

### 4.5 Visualisasi Peta Hasil Klasifikasi

Visualisasi peta hasil klasifikasi bertujuan menyajikan sebaran spasial kontinu kelas tutupan lahan di seluruh wilayah penelitian dengan menerapkan model Random Forest yang telah dilatih pada Subbab 4.2 ke seluruh bentang raster citra Sentinel-2 L2A komposit (`openEO.tif`).

**Prinsip dan Ketentuan Metodologis:**
1. **Model yang Digunakan:** Klasifikasi diterapkan secara langsung menggunakan model Random Forest (`rf_model`) yang telah dilatih pada data latih Bab 4 tanpa pelatihan ulang.
2. **Kesesuaian Fitur Spektral:** Seluruh piksel valid diproses dengan mengekstrak 4 band reflektansi (`B03`, `B04`, `B08`, `B11`) serta 3 indeks spektral rasio normalisasi (`NDVI`, `NDWI`, `NDBI`) menggunakan formula dan urutan kolom fitur yang persis sama dengan dataset pelatihan.
3. **Penanganan NoData dan Georeferensi:** Piksel bernilai NoData (-32768) atau tak hingga disaring dan diberi kode 0 (*NoData*). Hasil klasifikasi dikonversi menjadi raster integer diskret (1: `built_up`, 2: `farmland`, 3: `water_body`, 4: `forest`, 5: `mangrove`), kemudian diekspor ke format GeoTIFF terkompresi LZW (`hasil_klasifikasi_rf.tif`) dengan mempertahankan sistem koordinat terproyeksi asli (`EPSG:32750`, WGS 84 / UTM Zone 50S), batas wilayah, serta resolusi spasial 20 meter.
4. **Peta Interaktif Folium:** Raster klasifikasi direproeksi ke sistem koordinat geografis WGS 84 (`EPSG:4326`) untuk ditampilkan sebagai layer overlay transparan di atas basemap citra satelit resolusi tinggi *Esri World Imagery* dan *OpenStreetMap*. Peta dilengkapi kontrol pemilih layer (*LayerControl*) per kelas tutupan lahan dan legenda tematik yang konsisten.
5. **Independensi dari Sampel Poligon:** Visualisasi ini murni menampilkan inferensi piksel raster mandiri dari model Random Forest, bukan hasil penggambaran ulang poligon sampel GeoJSON.


```python
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier

# --- 1. Konfigurasi Path dan Verifikasi Model RF ---
DATA_DIR    = Path(r'C:\Users\Alif\PSD')
CITRA_PATH  = DATA_DIR / 'hasil_sentinel2' / 'openEO.tif'
OUT_TIF     = DATA_DIR / 'hasil_klasifikasi_rf.tif'
NODATA_VAL  = -32768

# Pastikan model rf_model tersedia (menggunakan instance dari Subbab 4.2)
if 'rf_model' not in globals():
    df_train_tmp = pd.read_csv(DATA_DIR / 'dataset_latih_70.csv')
    FITUR_COLS_TMP = ['B03', 'B04', 'B08', 'B11', 'NDVI', 'NDWI', 'NDBI']
    rf_model = RandomForestClassifier(
        n_estimators=200, max_features='sqrt', min_samples_leaf=1,
        oob_score=True, random_state=42, n_jobs=-1
    )
    rf_model.fit(df_train_tmp[FITUR_COLS_TMP], df_train_tmp['kelas'])

print('=== 1. MEMBACA RASTER CITRA SENTINEL-2 DAN MENYIAPKAN FITUR ===')
with rasterio.open(CITRA_PATH) as src:
    citra_meta      = src.meta.copy()
    src_crs         = src.crs
    src_transform   = src.transform
    src_bounds      = src.bounds
    res_x, res_y    = src.res
    h_ras, w_ras    = src.height, src.width

    # Muat ke memori sebagai float32 untuk komputasi spektral
    b03 = src.read(1).astype('float32')
    b04 = src.read(2).astype('float32')
    b08 = src.read(3).astype('float32')
    b11 = src.read(4).astype('float32')

print(f'Dimensi Citra Raster : {w_ras} x {h_ras} piksel (Total: {w_ras * h_ras:,} piksel)')
print(f'Sistem Koordinat     : {src_crs}')
print(f'Resolusi Spasial     : {res_x:.1f} m x {res_y:.1f} m ({res_x * res_y:.0f} m2 per piksel)')
print(f'Batas Spasial (UTM)  : X=[{src_bounds.left:.1f}, {src_bounds.right:.1f}], Y=[{src_bounds.bottom:.1f}, {src_bounds.top:.1f}]')

# --- 2. Mask Piksel Valid (Bebas NoData dan Nilai Tak Hingga) ---
valid_mask = (b03 != NODATA_VAL) & (b04 != NODATA_VAL) & (b08 != NODATA_VAL) & (b11 != NODATA_VAL)
valid_mask &= np.isfinite(b03) & np.isfinite(b04) & np.isfinite(b08) & np.isfinite(b11)

n_valid_px  = int(valid_mask.sum())
n_total_px  = w_ras * h_ras
n_nodata_px = n_total_px - n_valid_px

print(f'\nPiksel Valid Siap Prediksi : {n_valid_px:,} ({n_valid_px / n_total_px * 100:.2f}%)')
print(f'Piksel NoData / Invalid    : {n_nodata_px:,} ({n_nodata_px / n_total_px * 100:.4f}%)')

# --- 3. Ekstraksi Fitur Spektral pada Piksel Valid ---
px_b03 = b03[valid_mask]
px_b04 = b04[valid_mask]
px_b08 = b08[valid_mask]
px_b11 = b11[valid_mask]

def hitung_rasio(a, b):
    penyebut = a + b
    hasil = np.where(penyebut != 0, (a - b) / penyebut, 0.0)
    return hasil

px_ndvi = hitung_rasio(px_b08, px_b04)  # (NIR - Red) / (NIR + Red)
px_ndwi = hitung_rasio(px_b03, px_b08)  # (Green - NIR) / (Green + NIR)
px_ndbi = hitung_rasio(px_b11, px_b08)  # (SWIR - NIR) / (SWIR + NIR)

# Bentuk DataFrame dengan urutan kolom fitur yang persis sama seperti saat pelatihan
X_raster = pd.DataFrame({
    'B03': px_b03,
    'B04': px_b04,
    'B08': px_b08,
    'B11': px_b11,
    'NDVI': px_ndvi,
    'NDWI': px_ndwi,
    'NDBI': px_ndbi
})

# --- 4. Klasifikasi Seluruh Piksel Valid Menggunakan Random Forest Bab 4 ---
print('\n=== 2. MENJALANKAN INFERENSI MODEL RANDOM FOREST ===')
y_pred_raster = rf_model.predict(X_raster)

# Pemetaan kelas ke integer diskret
CLASS_MAP = {'built_up': 1, 'farmland': 2, 'water_body': 3, 'forest': 4, 'mangrove': 5}
INV_MAP   = {v: k for k, v in CLASS_MAP.items()}

pred_int = np.array([CLASS_MAP[k] for k in y_pred_raster], dtype=np.uint8)

# Rekonstruksi array 2D raster klasifikasi
classified_raster = np.zeros((h_ras, w_ras), dtype=np.uint8)
classified_raster[valid_mask] = pred_int

# --- 5. Ekspor Hasil Klasifikasi ke Berkas GeoTIFF ---
out_meta = citra_meta.copy()
out_meta.update({
    'driver': 'GTiff',
    'dtype': 'uint8',
    'count': 1,
    'nodata': 0,
    'compress': 'lzw'
})

with rasterio.open(OUT_TIF, 'w', **out_meta) as dst:
    dst.write(classified_raster, 1)

print(f'Raster hasil klasifikasi berhasil diekspor ke: {OUT_TIF}')
print(f'Ukuran berkas GeoTIFF: {OUT_TIF.stat().st_size / 1024:.1f} KB (terkompresi LZW)')

# --- 6. Ringkasan Distribusi Spasial dan Luas Area per Kelas ---
pixel_area_ha  = (res_x * res_y) / 10000.0  # 400 m2 = 0.04 ha
pixel_area_km2 = pixel_area_ha / 100.0     # 0.0004 km2

dist_rows = []
for cid in range(1, 6):
    cname    = INV_MAP[cid]
    count    = int((classified_raster == cid).sum())
    pct      = (count / n_valid_px) * 100.0
    area_ha  = count * pixel_area_ha
    area_km2 = count * pixel_area_km2
    dist_rows.append({
        'Kode': cid,
        'Kelas Tutupan Lahan': cname,
        'Jumlah Piksel': f'{count:,}',
        'Proporsi (%)': f'{pct:.2f}%',
        'Luas (ha)': f'{area_ha:,.1f}',
        'Luas (km2)': f'{area_km2:,.2f}'
    })

df_dist_raster = pd.DataFrame(dist_rows)
print('\n--- Distribusi Spasial Hasil Klasifikasi Tutupan Lahan ---')
print(df_dist_raster.to_string(index=False))
```

    === 1. MEMBACA RASTER CITRA SENTINEL-2 DAN MENYIAPKAN FITUR ===
    Dimensi Citra Raster : 1352 x 1477 piksel (Total: 1,996,904 piksel)
    Sistem Koordinat     : EPSG:32750
    Resolusi Spasial     : 20.0 m x 20.0 m (400 m2 per piksel)
    Batas Spasial (UTM)  : X=[206700.0, 233740.0], Y=[9037110.0, 9066650.0]
    
    Piksel Valid Siap Prediksi : 1,996,816 (100.00%)
    Piksel NoData / Invalid    : 88 (0.0044%)
    
    === 2. MENJALANKAN INFERENSI MODEL RANDOM FOREST ===
    Raster hasil klasifikasi berhasil diekspor ke: C:\Users\Alif\PSD\hasil_klasifikasi_rf.tif
    Ukuran berkas GeoTIFF: 108.1 KB (terkompresi LZW)
    
    --- Distribusi Spasial Hasil Klasifikasi Tutupan Lahan ---
     Kode Kelas Tutupan Lahan Jumlah Piksel Proporsi (%) Luas (ha) Luas (km2)
        1            built_up        33,519        1.68%   1,340.8      13.41
        2            farmland        91,600        4.59%   3,664.0      36.64
        3          water_body     1,243,115       62.25%  49,724.6     497.25
        4              forest       585,992       29.35%  23,439.7     234.40
        5            mangrove        42,590        2.13%   1,703.6      17.04
    


```python
import folium
from folium.raster_layers import ImageOverlay
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
from pathlib import Path

DATA_DIR = Path(r'C:\Users\Alif\PSD')
OUT_HTML = DATA_DIR / 'Peta_Hasil_Klasifikasi_RF.html'

print('=== 3. MEMBANGUN PETA INTERAKTIF OVERLAY CITRA SATELIT ===')

# --- 1. Reproeksi Raster Klasifikasi ke WGS 84 (EPSG:4326) untuk Folium ---
dst_crs = 'EPSG:4326'
transform_4326, width_4326, height_4326 = calculate_default_transform(
    src_crs, dst_crs, w_ras, h_ras, *src_bounds
)

classified_4326 = np.zeros((height_4326, width_4326), dtype=np.uint8)

reproject(
    source=classified_raster,
    destination=classified_4326,
    src_transform=src_transform,
    src_crs=src_crs,
    dst_transform=transform_4326,
    dst_crs=dst_crs,
    resampling=Resampling.nearest,  # Nearest neighbor wajib untuk kelas diskret
    src_nodata=0,
    dst_nodata=0
)

# Hitung koordinat batas (bounding box lat/lon)
left_lon   = transform_4326[2]
top_lat    = transform_4326[5]
right_lon  = left_lon + width_4326 * transform_4326[0]
bottom_lat = top_lat + height_4326 * transform_4326[4]
folium_bounds = [[bottom_lat, left_lon], [top_lat, right_lon]]

center_lat = (bottom_lat + top_lat) / 2
center_lon = (left_lon + right_lon) / 2

print(f'Pusat Peta (Lat, Lon) : [{center_lat:.5f}, {center_lon:.5f}]')
print(f'Batas Geografis (WGS84): Selatan={bottom_lat:.4f}, Barat={left_lon:.4f}, Utara={top_lat:.4f}, Timur={right_lon:.4f}')

# --- 2. Inisialisasi Peta Folium ---
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=11,
    tiles=None,
    control_scale=True
)

# --- 3. Basemaps Pilihan (Satelit dan OpenStreetMap) ---
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri World Imagery',
    name='Citra Satelit (Esri World Imagery)',
    overlay=False,
    control=True
).add_to(m)

folium.TileLayer(
    tiles='OpenStreetMap',
    name='OpenStreetMap (Peta Jalan)',
    overlay=False,
    control=True
).add_to(m)

# --- 4. Palet Warna Standar Klasifikasi ---
COLOR_CONFIG = {
    1: ('built_up',   'Lahan Terbangun',  [228, 26, 28]),     # Merah
    2: ('farmland',   'Lahan Pertanian',  [230, 171, 2]),     # Kuning-Emas / Oranye
    3: ('water_body', 'Badan Air',        [31, 120, 180]),    # Biru
    4: ('forest',     'Hutan Alami',      [34, 139, 34]),     # Hijau Tua
    5: ('mangrove',   'Hutan Mangrove',   [0, 168, 132])      # Toska / Cyan Green
}

# --- 5. Layer Overlay Klasifikasi Lengkap (Semua Kelas) ---
rgba_all = np.zeros((height_4326, width_4326, 4), dtype=np.uint8)
for cid, (cname, clabel, rgb) in COLOR_CONFIG.items():
    mask = (classified_4326 == cid)
    rgba_all[mask, :3] = rgb
    rgba_all[mask, 3]  = 180  # Opasitas ~70% agar kontur permukaan satelit terlihat

ImageOverlay(
    image=rgba_all,
    bounds=folium_bounds,
    opacity=0.75,
    name='Klasifikasi RF: Semua Kelas',
    overlay=True,
    control=True,
    show=True
).add_to(m)

# --- 6. Layer Overlay Terpisah per Kelas (Dapat Dicentang di LayerControl) ---
for cid, (cname, clabel, rgb) in COLOR_CONFIG.items():
    rgba_cls = np.zeros((height_4326, width_4326, 4), dtype=np.uint8)
    mask = (classified_4326 == cid)
    rgba_cls[mask, :3] = rgb
    rgba_cls[mask, 3]  = 200

    ImageOverlay(
        image=rgba_cls,
        bounds=folium_bounds,
        opacity=0.8,
        name=f'Layer Kelas: {cname} ({clabel})',
        overlay=True,
        control=True,
        show=False  # Non-aktif secara default agar tidak bertumpuk
    ).add_to(m)

# --- 7. Elemen Legenda Peta (Floating Thematic Legend) ---
legend_html = '''
<div style="
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 250px;
    z-index: 9999;
    background-color: rgba(255, 255, 255, 0.95);
    border: 2px solid #555;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    font-family: Arial, sans-serif;
">
<b style="font-size: 14px; color: #222;">Legenda Tutupan Lahan</b><br>
<span style="font-size: 11px; color: #666;">Prediksi Model Random Forest</span>
<hr style="margin: 8px 0; border: 0; border-top: 1px solid #ccc;">
<div style="margin-bottom: 5px;">
    <span style="display:inline-block; width:16px; height:16px; background:rgb(228,26,28); border-radius:3px; vertical-align:middle; margin-right:8px;"></span>
    <b>built_up</b> <span style="font-size:11px; color:#555;">(Lahan Terbangun)</span>
</div>
<div style="margin-bottom: 5px;">
    <span style="display:inline-block; width:16px; height:16px; background:rgb(230,171,2); border-radius:3px; vertical-align:middle; margin-right:8px;"></span>
    <b>farmland</b> <span style="font-size:11px; color:#555;">(Lahan Pertanian)</span>
</div>
<div style="margin-bottom: 5px;">
    <span style="display:inline-block; width:16px; height:16px; background:rgb(31,120,180); border-radius:3px; vertical-align:middle; margin-right:8px;"></span>
    <b>water_body</b> <span style="font-size:11px; color:#555;">(Badan Air / Laut)</span>
</div>
<div style="margin-bottom: 5px;">
    <span style="display:inline-block; width:16px; height:16px; background:rgb(34,139,34); border-radius:3px; vertical-align:middle; margin-right:8px;"></span>
    <b>forest</b> <span style="font-size:11px; color:#555;">(Hutan Alami)</span>
</div>
<div style="margin-bottom: 5px;">
    <span style="display:inline-block; width:16px; height:16px; background:rgb(0,168,132); border-radius:3px; vertical-align:middle; margin-right:8px;"></span>
    <b>mangrove</b> <span style="font-size:11px; color:#555;">(Hutan Mangrove)</span>
</div>
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# --- 8. Kontrol Layer ---
folium.LayerControl(collapsed=False).add_to(m)

# Simpan ke berkas HTML mandiri
m.save(str(OUT_HTML))
print(f'Peta interaktif berhasil disimpan ke berkas HTML: {OUT_HTML}')
print('Menampilkan peta interaktif langsung pada sel notebook...')

# Tampilkan objek peta agar ter-render langsung di Jupyter Notebook
m
```

    === 3. MEMBANGUN PETA INTERAKTIF OVERLAY CITRA SATELIT ===
    Pusat Peta (Lat, Lon) : [-8.56894, 114.45823]
    Batas Geografis (WGS84): Selatan=-8.7032, Barat=114.3346, Utara=-8.4346, Timur=114.5818
    Peta interaktif berhasil disimpan ke berkas HTML: C:\Users\Alif\PSD\Peta_Hasil_Klasifikasi_RF.html
    Menampilkan peta interaktif langsung pada sel notebook...
    




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe srcdoc="&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;

    &lt;meta http-equiv=&quot;content-type&quot; content=&quot;text/html; charset=UTF-8&quot; /&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://code.jquery.com/jquery-3.7.1.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js&quot;&gt;&lt;/script&gt;
    &lt;script src=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js&quot;&gt;&lt;/script&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap-glyphicons.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.0/css/all.min.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css&quot;/&gt;
    &lt;link rel=&quot;stylesheet&quot; href=&quot;https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css&quot;/&gt;

            &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width,
                initial-scale=1.0, maximum-scale=1.0, user-scalable=no&quot; /&gt;
            &lt;style&gt;
                #map_42964b3396feac99b5ba42b35536e68d {
                    position: relative;
                    width: 100.0%;
                    height: 100.0%;
                    left: 0.0%;
                    top: 0.0%;
                }
                .leaflet-container { font-size: 1rem; }
            &lt;/style&gt;

            &lt;style&gt;html, body {
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
            }
            &lt;/style&gt;

            &lt;style&gt;#map {
                position:absolute;
                top:0;
                bottom:0;
                right:0;
                left:0;
                }
            &lt;/style&gt;

            &lt;script&gt;
                L_NO_TOUCH = false;
                L_DISABLE_3D = false;
            &lt;/script&gt;




                &lt;style&gt;
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                &lt;/style&gt;




                &lt;style&gt;
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                &lt;/style&gt;




                &lt;style&gt;
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                &lt;/style&gt;




                &lt;style&gt;
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                &lt;/style&gt;




                &lt;style&gt;
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                &lt;/style&gt;




                &lt;style&gt;
                    .leaflet-image-layer {
                        /* old android/safari*/
                        image-rendering: -webkit-optimize-contrast;
                        image-rendering: crisp-edges; /* safari */
                        image-rendering: pixelated; /* chrome */
                        image-rendering: -moz-crisp-edges; /* firefox */
                        image-rendering: -o-crisp-edges; /* opera */
                        -ms-interpolation-mode: nearest-neighbor; /* ie */
                    }
                &lt;/style&gt;


&lt;/head&gt;
&lt;body&gt;


&lt;div style=&quot;
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 250px;
    z-index: 9999;
    background-color: rgba(255, 255, 255, 0.95);
    border: 2px solid #555;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
    font-family: Arial, sans-serif;
&quot;&gt;
&lt;b style=&quot;font-size: 14px; color: #222;&quot;&gt;Legenda Tutupan Lahan&lt;/b&gt;&lt;br&gt;
&lt;span style=&quot;font-size: 11px; color: #666;&quot;&gt;Prediksi Model Random Forest&lt;/span&gt;
&lt;hr style=&quot;margin: 8px 0; border: 0; border-top: 1px solid #ccc;&quot;&gt;
&lt;div style=&quot;margin-bottom: 5px;&quot;&gt;
    &lt;span style=&quot;display:inline-block; width:16px; height:16px; background:rgb(228,26,28); border-radius:3px; vertical-align:middle; margin-right:8px;&quot;&gt;&lt;/span&gt;
    &lt;b&gt;built_up&lt;/b&gt; &lt;span style=&quot;font-size:11px; color:#555;&quot;&gt;(Lahan Terbangun)&lt;/span&gt;
&lt;/div&gt;
&lt;div style=&quot;margin-bottom: 5px;&quot;&gt;
    &lt;span style=&quot;display:inline-block; width:16px; height:16px; background:rgb(230,171,2); border-radius:3px; vertical-align:middle; margin-right:8px;&quot;&gt;&lt;/span&gt;
    &lt;b&gt;farmland&lt;/b&gt; &lt;span style=&quot;font-size:11px; color:#555;&quot;&gt;(Lahan Pertanian)&lt;/span&gt;
&lt;/div&gt;
&lt;div style=&quot;margin-bottom: 5px;&quot;&gt;
    &lt;span style=&quot;display:inline-block; width:16px; height:16px; background:rgb(31,120,180); border-radius:3px; vertical-align:middle; margin-right:8px;&quot;&gt;&lt;/span&gt;
    &lt;b&gt;water_body&lt;/b&gt; &lt;span style=&quot;font-size:11px; color:#555;&quot;&gt;(Badan Air / Laut)&lt;/span&gt;
&lt;/div&gt;
&lt;div style=&quot;margin-bottom: 5px;&quot;&gt;
    &lt;span style=&quot;display:inline-block; width:16px; height:16px; background:rgb(34,139,34); border-radius:3px; vertical-align:middle; margin-right:8px;&quot;&gt;&lt;/span&gt;
    &lt;b&gt;forest&lt;/b&gt; &lt;span style=&quot;font-size:11px; color:#555;&quot;&gt;(Hutan Alami)&lt;/span&gt;
&lt;/div&gt;
&lt;div style=&quot;margin-bottom: 5px;&quot;&gt;
    &lt;span style=&quot;display:inline-block; width:16px; height:16px; background:rgb(0,168,132); border-radius:3px; vertical-align:middle; margin-right:8px;&quot;&gt;&lt;/span&gt;
    &lt;b&gt;mangrove&lt;/b&gt; &lt;span style=&quot;font-size:11px; color:#555;&quot;&gt;(Hutan Mangrove)&lt;/span&gt;
&lt;/div&gt;
&lt;/div&gt;

            &lt;div class=&quot;folium-map&quot; id=&quot;map_42964b3396feac99b5ba42b35536e68d&quot; &gt;&lt;/div&gt;

&lt;/body&gt;
&lt;script&gt;


            var map_42964b3396feac99b5ba42b35536e68d = L.map(
                &quot;map_42964b3396feac99b5ba42b35536e68d&quot;,
                {
                    center: [-8.56894225243153, 114.45823091555332],
                    crs: L.CRS.EPSG3857,
                    ...{
  &quot;zoom&quot;: 11,
  &quot;zoomControl&quot;: true,
  &quot;preferCanvas&quot;: false,
}

                }
            );
            L.control.scale().addTo(map_42964b3396feac99b5ba42b35536e68d);





            var tile_layer_95d03788027d4213ac126b3e6cc7b676 = L.tileLayer(
                &quot;https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}&quot;,
                {
  &quot;minZoom&quot;: 0,
  &quot;maxZoom&quot;: 18,
  &quot;maxNativeZoom&quot;: 18,
  &quot;noWrap&quot;: false,
  &quot;attribution&quot;: &quot;Esri World Imagery&quot;,
  &quot;subdomains&quot;: &quot;abc&quot;,
  &quot;detectRetina&quot;: false,
  &quot;tms&quot;: false,
  &quot;opacity&quot;: 1,
}

            );


            tile_layer_95d03788027d4213ac126b3e6cc7b676.addTo(map_42964b3396feac99b5ba42b35536e68d);


            var tile_layer_162722119e63c511e72e0a6bec822c5c = L.tileLayer(
                &quot;https://tile.openstreetmap.org/{z}/{x}/{y}.png&quot;,
                {
  &quot;minZoom&quot;: 0,
  &quot;maxZoom&quot;: 19,
  &quot;maxNativeZoom&quot;: 19,
  &quot;noWrap&quot;: false,
  &quot;attribution&quot;: &quot;\u0026copy; \u003ca href=\&quot;https://www.openstreetmap.org/copyright\&quot;\u003eOpenStreetMap\u003c/a\u003e contributors&quot;,
  &quot;subdomains&quot;: &quot;abc&quot;,
  &quot;detectRetina&quot;: false,
  &quot;tms&quot;: false,
  &quot;opacity&quot;: 1,
}

            );


            tile_layer_162722119e63c511e72e0a6bec822c5c.addTo(map_42964b3396feac99b5ba42b35536e68d);


            var image_overlay_a6b9ec225efe8a21ef45306867c53a93 = L.imageOverlay(
                &quot;data:image/png;base64,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&quot;,
                [[-8.703235516498252, 114.33462315732602], [-8.434648988364806, 114.58183867378061]],
                {
  &quot;opacity&quot;: 0.75,
}
            );


            image_overlay_a6b9ec225efe8a21ef45306867c53a93.addTo(map_42964b3396feac99b5ba42b35536e68d);


            var image_overlay_4f0020f8cbf5a7c1fda146a06bde5b19 = L.imageOverlay(
                &quot;data:image/png;base64,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&quot;,
                [[-8.703235516498252, 114.33462315732602], [-8.434648988364806, 114.58183867378061]],
                {
  &quot;opacity&quot;: 0.8,
}
            );


            var image_overlay_659733fffc648dd0650b831d3de905ba = L.imageOverlay(
                &quot;data:image/png;base64,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&quot;,
                [[-8.703235516498252, 114.33462315732602], [-8.434648988364806, 114.58183867378061]],
                {
  &quot;opacity&quot;: 0.8,
}
            );


            var image_overlay_3a502a025bce8e4653403d7223f3fc33 = L.imageOverlay(
                &quot;data:image/png;base64,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&quot;,
                [[-8.703235516498252, 114.33462315732602], [-8.434648988364806, 114.58183867378061]],
                {
  &quot;opacity&quot;: 0.8,
}
            );


            var image_overlay_38a084ac86046143804b4206ae230d7b = L.imageOverlay(
                &quot;data:image/png;base64,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&quot;,
                [[-8.703235516498252, 114.33462315732602], [-8.434648988364806, 114.58183867378061]],
                {
  &quot;opacity&quot;: 0.8,
}
            );


            var image_overlay_7cdfa85d73b5e07c8ef24930ae1f7866 = L.imageOverlay(
                &quot;data:image/png;base64,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&quot;,
                [[-8.703235516498252, 114.33462315732602], [-8.434648988364806, 114.58183867378061]],
                {
  &quot;opacity&quot;: 0.8,
}
            );


            var layer_control_9ede2a4d1a343e0e5a14b67fb09adb9c_layers = {
                base_layers : {
                    &quot;Citra Satelit (Esri World Imagery)&quot; : tile_layer_95d03788027d4213ac126b3e6cc7b676,
                    &quot;OpenStreetMap (Peta Jalan)&quot; : tile_layer_162722119e63c511e72e0a6bec822c5c,
                },
                overlays :  {
                    &quot;Klasifikasi RF: Semua Kelas&quot; : image_overlay_a6b9ec225efe8a21ef45306867c53a93,
                    &quot;Layer Kelas: built_up (Lahan Terbangun)&quot; : image_overlay_4f0020f8cbf5a7c1fda146a06bde5b19,
                    &quot;Layer Kelas: farmland (Lahan Pertanian)&quot; : image_overlay_659733fffc648dd0650b831d3de905ba,
                    &quot;Layer Kelas: water_body (Badan Air)&quot; : image_overlay_3a502a025bce8e4653403d7223f3fc33,
                    &quot;Layer Kelas: forest (Hutan Alami)&quot; : image_overlay_38a084ac86046143804b4206ae230d7b,
                    &quot;Layer Kelas: mangrove (Hutan Mangrove)&quot; : image_overlay_7cdfa85d73b5e07c8ef24930ae1f7866,
                },
            };
            let layer_control_9ede2a4d1a343e0e5a14b67fb09adb9c = L.control.layers(
                layer_control_9ede2a4d1a343e0e5a14b67fb09adb9c_layers.base_layers,
                layer_control_9ede2a4d1a343e0e5a14b67fb09adb9c_layers.overlays,
                {
  &quot;position&quot;: &quot;topright&quot;,
  &quot;collapsed&quot;: false,
  &quot;autoZIndex&quot;: true,
}
            ).addTo(map_42964b3396feac99b5ba42b35536e68d);



            tile_layer_95d03788027d4213ac126b3e6cc7b676.addTo(map_42964b3396feac99b5ba42b35536e68d);


            tile_layer_162722119e63c511e72e0a6bec822c5c.addTo(map_42964b3396feac99b5ba42b35536e68d);


            image_overlay_a6b9ec225efe8a21ef45306867c53a93.addTo(map_42964b3396feac99b5ba42b35536e68d);

&lt;/script&gt;
&lt;/html&gt;" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



#### Analisis Hasil Visualisasi Peta dan Keterbatasan Spasial

Berdasarkan visualisasi spasial kontinu di atas, diperoleh wawasan penting mengenai sebaran kelas tutupan lahan hasil prediksi model:
1. **Pola Spasial Alami:**
   - **`water_body` (62,25% / 497,25 km²):** Mendominasi perairan terbuka di Teluk Pangpang serta perairan laut lepas Selat Bali dan Samudera Hindia di sebelah timur dan selatan semenanjung.
   - **`forest` (29,35% / 234,40 km²):** Terkonsentrasi kuat dan kompak di kawasan lindung Taman Nasional Alas Purwo pada bagian timur dan selatan semenanjung Blambangan, terpisah tegas dari lahan budidaya.
   - **`mangrove` (2,13% / 17,04 km²):** Berada secara konsisten menyusuri zona intertidal dan muara sungai di Teluk Pangpang sebagai vegetasi penyangga pesisir (*coastal buffer*).
   - **`farmland` (4,59% / 36,64 km²):** Tersebar luas di dataran aluvial pertanian intensif di bagian barat wilayah kajian (Tegaldlimo dan Muncar).
   - **`built_up` (1,68% / 13,41 km²):** Terpetakan secara terfokus pada pusat-pusat permukiman padat dan pelabuhan Muncar serta desa-desa di Tegaldlimo.

2. **Perbedaan Mendasar dari Poligon Sampel:**
   Peta di atas merepresentasikan hasil inferensi mandiri (*pixel-wise inference*) dari seluruh 1.996.816 piksel citra Sentinel-2 berdasar respons spektral kontinu, bukan hasil proyeksi atau penggambaran ulang poligon sampel GeoJSON. Batas-batas tutupan lahan yang terbentuk mengikuti dinamika lanskap aktual di lapangan.

3. **Cakupan Aktual dan Batasan Geografis:**
   Raster citra Sentinel-2 yang tersedia mencakup area seluas **798,74 km²** (lebar 27,04 km, tinggi 29,54 km) di sekitar Muncar, Teluk Pangpang, Tegaldlimo, dan Alas Purwo, Kabupaten Banyuwangi. Peta ini secara objektif hanya menampilkan wilayah yang tercakup dalam data raster aktual tanpa menambahkan prediksi sintetis atau interpolasi fiktif di luar jangkauan citra.


```python
import joblib

# Simpan model Random Forest yang sudah dilatih
joblib.dump(rf_model, "random_forest_model.pkl")

print("Model Random Forest berhasil disimpan.")
```

    Model Random Forest berhasil disimpan.
    

## 5. Evaluation

Tahap *Evaluation* bertujuan menguji dan memvalidasi model klasifikasi Random Forest secara mendalam menggunakan data uji (*test set*, $N = 152$) yang telah dipisahkan secara independen pada level poligon (*polygon-level split*) di Bab 3. Evaluasi ini dilakukan tanpa melatih ulang model atau memodifikasi parameter model yang telah ditetapkan pada Bab 4.

Evaluasi disajikan melalui empat subbab terstruktur:
1. **Evaluasi Kinerja Model:** Perhitungan metrik kuantitatif formal (*accuracy*, *precision*, *recall*, dan *F1-score*) baik per kelas maupun agregat (*macro average* dan *weighted average*).
2. **Confusion Matrix:** Penyajian matriks konfusi dengan urutan kelas yang konsisten dan visualisasi peta panas (*heatmap*).
3. **Analisis Hasil Klasifikasi:** Pembahasan detail temuan evaluasi, pemeriksaan distribusi kelas, serta audit mendalam terhadap galat misklasifikasi pada sampel individual.
4. **Interpretasi dan Keterbatasan Model:** Pembahasan kritis mengenai efek autokorelasi spasial, resolusi raster 20 meter, risiko *mixed pixel*, dampak `all_touched=True`, serta batasan generalisasi model dari AOI Banyuwangi ke tingkat regional Jawa Timur.Cakupan geografis juga menjadi keterbatasan penelitian. Data sampel dan raster yang digunakan berfokus pada wilayah Kabupaten Banyuwangi, sehingga hasil evaluasi belum cukup untuk menyimpulkan bahwa model memiliki tingkat kinerja yang sama pada seluruh wilayah Provinsi Jawa Timur. Perbedaan karakteristik tutupan lahan, kondisi geografis, dan respons spektral antardaerah dapat memengaruhi hasil klasifikasi. Pengujian pada wilayah lain dengan data referensi independen diperlukan untuk menilai kemampuan generalisasi model secara lebih luas.

### 5.1 Evaluasi Kinerja Model

Evaluasi performa klasifikasi tutupan lahan multikelas menggunakan metrik formal berbasis matriks kesalahan:

1. **Accuracy (Akurasi Menyeluruh):** Proporsi seluruh prediksi benar terhadap total sampel data uji.
   $$\text{Accuracy} = \frac{\sum_{k=1}^K TP_k}{N}$$
   Pada evaluasi ini, $N = 152$ sampel uji.

2. **Precision (Kemurnian Prediksi):** Proporsi sampel yang diprediksi sebagai kelas $k$ yang benar-benar merupakan kelas $k$.
   $$\text{Precision}_k = \frac{TP_k}{TP_k + FP_k}$$
   Mengukur resistansi model terhadap kesalahan komisi (*false alarms*).

3. **Recall (Sensitivitas / Kelengkapan Deteksi):** Proporsi sampel aktual kelas $k$ yang berhasil diprediksi dengan benar oleh model.
   $$\text{Recall}_k = \frac{TP_k}{TP_k + FN_k}$$
   Mengukur kemampuan model mendeteksi seluruh anggota kelas tanpa kesalahan omisi. Metrik ini setara dengan *Producer's Accuracy* pada literatur penginderaan jauh.

4. **F1-Score:** Rata-rata harmonik antara *precision* dan *recall*, memberikan ukuran keseimbangan kinerja terutama jika terdapat galat yang asimetris.
   $$F_1 = 2 \times \frac{\text{Precision}_k \times \text{Recall}_k}{\text{Precision}_k + \text{Recall}_k}$$

5. **Macro Average:** Rata-rata aritmatika tidak tertimbang (*unweighted mean*) dari metrik setiap kelas tanpa memperhitungkan jumlah sampel:
   $$\text{Macro Metric} = \frac{1}{K} \sum_{k=1}^K \text{Metric}_k$$
   Memberikan bobot setara pada setiap kelas, sehingga sensitif terhadap penurunan kinerja pada kelas tertentu.

6. **Weighted Average:** Rata-rata tertimbang berdasarkan jumlah sampel aktual (*support*) masing-masing kelas:
   $$\text{Weighted Metric} = \sum_{k=1}^K \left(\frac{N_k}{N}\right) \text{Metric}_k$$


```python
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report
)

# --- 1. Muat Hasil Prediksi Data Uji Aktual Bab 4 ---
DATA_DIR   = Path(r'C:\Users\Alif\PSD')
KELAS_URUT = ['built_up', 'farmland', 'water_body', 'forest', 'mangrove']

df_hasil = pd.read_csv(DATA_DIR / 'hasil_prediksi_rf.csv')
y_true = df_hasil['kelas']
y_pred = df_hasil['y_pred']

# --- 2. Hitung Metrik Evaluasi per Kelas ---
report_dict = classification_report(y_true, y_pred, labels=KELAS_URUT, output_dict=True, zero_division=0)

rows_kelas = []
for k in KELAS_URUT:
    tp = int(((y_true == k) & (y_pred == k)).sum())
    fp = int(((y_true != k) & (y_pred == k)).sum())
    fn = int(((y_true == k) & (y_pred != k)).sum())
    support = int((y_true == k).sum())
    prec = report_dict[k]['precision']
    rec = report_dict[k]['recall']
    f1 = report_dict[k]['f1-score']
    
    rows_kelas.append({
        'Kelas': k,
        'TP': tp,
        'FP': fp,
        'FN': fn,
        'Support': support,
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1-Score': round(f1, 4)
    })

df_metrik_kelas = pd.DataFrame(rows_kelas)

# --- 3. Hitung Ringkasan Metrik Agregat ---
acc_val = accuracy_score(y_true, y_pred)
macro_p = report_dict['macro avg']['precision']
macro_r = report_dict['macro avg']['recall']
macro_f1 = report_dict['macro avg']['f1-score']

weighted_p = report_dict['weighted avg']['precision']
weighted_r = report_dict['weighted avg']['recall']
weighted_f1 = report_dict['weighted avg']['f1-score']

df_agregat = pd.DataFrame([
    {'Metrik Evaluasi': 'Accuracy', 'Precision': '-', 'Recall': '-', 'F1-Score': f"{acc_val:.4f} ({acc_val*100:.2f}%)", 'Support': len(y_true)},
    {'Metrik Evaluasi': 'Macro Average', 'Precision': f"{macro_p:.4f} ({macro_p*100:.2f}%)", 'Recall': f"{macro_r:.4f} ({macro_r*100:.2f}%)", 'F1-Score': f"{macro_f1:.4f}", 'Support': len(y_true)},
    {'Metrik Evaluasi': 'Weighted Average', 'Precision': f"{weighted_p:.4f} ({weighted_p*100:.2f}%)", 'Recall': f"{weighted_r:.4f} ({weighted_r*100:.2f}%)", 'F1-Score': f"{weighted_f1:.4f}", 'Support': len(y_true)}
])

print('=== 5.1 METRIK EVALUASI KINERJA MODEL RANDOM FOREST ===')
print(f'Total Sampel Uji (N) : {len(y_true)}')
print(f'Prediksi Benar       : {(y_true == y_pred).sum()}')
print(f'Prediksi Salah       : {(y_true != y_pred).sum()}')
print(f'Akurasi Keseluruhan  : {acc_val:.4f} ({acc_val*100:.2f}%)\n')

print('--- Tabel Kinerja per Kelas Tutupan Lahan ---')
print(df_metrik_kelas.to_string(index=False))

print('\n--- Ringkasan Metrik Agregat ---')
print(df_agregat.to_string(index=False))
```

    === 5.1 METRIK EVALUASI KINERJA MODEL RANDOM FOREST ===
    Total Sampel Uji (N) : 152
    Prediksi Benar       : 151
    Prediksi Salah       : 1
    Akurasi Keseluruhan  : 0.9934 (99.34%)
    
    --- Tabel Kinerja per Kelas Tutupan Lahan ---
         Kelas  TP  FP  FN  Support  Precision  Recall  F1-Score
      built_up  30   0   0       30     1.0000  1.0000    1.0000
      farmland  30   0   0       30     1.0000  1.0000    1.0000
    water_body  31   1   0       31     0.9688  1.0000    0.9841
        forest  30   0   0       30     1.0000  1.0000    1.0000
      mangrove  30   0   1       31     1.0000  0.9677    0.9836
    
    --- Ringkasan Metrik Agregat ---
     Metrik Evaluasi       Precision          Recall        F1-Score  Support
            Accuracy               -               - 0.9934 (99.34%)      152
       Macro Average 0.9938 (99.38%) 0.9935 (99.35%)          0.9935      152
    Weighted Average 0.9936 (99.36%) 0.9934 (99.34%)          0.9934      152
    

### 5.2 Confusion Matrix

*Confusion matrix* menyajikan tabulasi silang antara label kelas aktual (*ground truth*) pada sumbu vertikal dan label hasil prediksi model pada sumbu horizontal. Urutan kelas disusun secara konsisten di seluruh tabel dan visualisasi: `built_up`, `farmland`, `water_body`, `forest`, dan `mangrove`.

Pada matriks ini:
- **Diagonal utama** merepresentasikan prediksi benar (*True Positives*) untuk masing-masing kelas.
- **Elemen di luar diagonal utama** menunjukkan kesalahan klasifikasi berupa *omission error* (dilihat sepanjang baris aktual) dan *commission error* (dilihat sepanjang kolom prediksi).


```python
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# --- 1. Bentuk Confusion Matrix Berdasarkan Urutan Kelas ---
cm = confusion_matrix(y_true, y_pred, labels=KELAS_URUT)

df_cm = pd.DataFrame(
    cm,
    index=[f'Aktual: {k}' for k in KELAS_URUT],
    columns=[f'Pred: {k}' for k in KELAS_URUT]
)

print('=== TABEL CONFUSION MATRIX (DATA UJI, N = 152) ===')
print(df_cm.to_string())

# --- 2. Visualisasi Heatmap Confusion Matrix ---
fig, ax = plt.subplots(figsize=(8, 6.5))
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=KELAS_URUT)
disp.plot(cmap='Blues', values_format='d', ax=ax, colorbar=True)

ax.set_title('Confusion Matrix - Random Forest pada Data Uji (N = 152)\nKlasifikasi Tutupan Lahan Sentinel-2', fontsize=12, pad=15, fontweight='bold')
ax.set_xlabel('Kelas Prediksi', fontsize=11, labelpad=10, fontweight='semibold')
ax.set_ylabel('Kelas Aktual', fontsize=11, labelpad=10, fontweight='semibold')
plt.xticks(rotation=25, ha='right', fontsize=10)
plt.yticks(fontsize=10)
plt.tight_layout()

# Simpan visualisasi matriks ke disk
CM_IMG_PATH = DATA_DIR / 'confusion_matrix_rf.png'
plt.savefig(CM_IMG_PATH, dpi=300)
plt.show()

print(f'\nVisualisasi confusion matrix berhasil disimpan ke: {CM_IMG_PATH}')
```

    findfont: Failed to find font weight semibold for DejaVu Sans, now using 700.
    

    === TABEL CONFUSION MATRIX (DATA UJI, N = 152) ===
                        Pred: built_up  Pred: farmland  Pred: water_body  Pred: forest  Pred: mangrove
    Aktual: built_up                30               0                 0             0               0
    Aktual: farmland                 0              30                 0             0               0
    Aktual: water_body               0               0                31             0               0
    Aktual: forest                   0               0                 0            30               0
    Aktual: mangrove                 0               0                 1             0              30
    


    
![png](../img/output_52_2.png)
    


    
    Visualisasi confusion matrix berhasil disimpan ke: C:\Users\Alif\PSD\confusion_matrix_rf.png
    

Berdasarkan matriks konfusi di atas:
- Empat kelas tutupan lahan, yaitu `built_up` (30 sampel), `farmland` (30 sampel), `water_body` (31 sampel), dan `forest` (30 sampel), memiliki akurasi klasifikasi sempurna (**100%**) tanpa ada satu pun sampel yang tertukar.
- Satu-satunya pertukaran kelas yang terjadi pada seluruh data uji adalah antara **`mangrove`** dan **`water_body`**: sebanyak **1 sampel aktual `mangrove` salah diklasifikasikan sebagai `water_body`**.
- Tidak ditemukan kebingungan kelas antara vegetasi darat (`forest` atau `farmland`) dengan vegetasi pesisir (`mangrove`), maupun antara lahan terbangun (`built_up`) dengan lahan pertanian (`farmland`).

### 5.3 Analisis Hasil Klasifikasi

Evaluasi klasifikasi tidak dapat hanya bertumpu pada skor akurasi menyeluruh (99,34%). Diperlukan analisis mendalam terhadap distribusi kelas sampel uji serta audit terhadap sampel yang mengalami kesalahan prediksi.

#### 1. Analisis Keseimbangan Distribusi Sampel Uji
Distribusi sampel pada data uji terdiri atas:
- `built_up`: 30 sampel (19,74%)
- `farmland`: 30 sampel (19,74%)
- `water_body`: 31 sampel (20,39%)
- `forest`: 30 sampel (19,74%)
- `mangrove`: 31 sampel (20,39%)

Karena proporsi kelima kelas berada pada rentang 19,7% hingga 20,4%, dataset uji bersifat seimbang (*balanced dataset*). Oleh karena itu, metrik *macro average* (F1 = 0,9935) dan *weighted average* (F1 = 0,9934) memiliki nilai yang hampir identik dan tidak terdistorsi oleh kelas mayoritas.

#### 2. Audit Sampel yang Mengalami Kesalahan Prediksi
Dari 152 sampel uji, hanya terdapat 1 sampel yang salah diprediksi oleh model Random Forest. Sel berikut mengaudit secara detail identitas poligon, nilai fitur spektral, probabilitas prediksi ensemble, serta karakteristik fisik spasial dari sampel tersebut.


```python
# --- Audit Mendalam Sampel yang Mengalami Misklasifikasi ---
df_test = pd.read_csv(DATA_DIR / 'dataset_uji_30.csv')
FITUR_COLS = ['B03', 'B04', 'B08', 'B11', 'NDVI', 'NDWI', 'NDBI']

df_salah = df_hasil[~df_hasil['prediksi_benar']].copy()

print('=== AUDIT SAMPEL SALAH KLASIFIKASI ===')
cols_tampil = ['polygon_id', 'label_asli', 'kelas', 'y_pred', 'prob_mangrove', 'prob_water_body', 'luas_m2', 'n_valid_px']
print(df_salah[cols_tampil].to_string(index=False))

# Ambil nilai spektral poligon yang salah dari dataset uji
salah_id = df_salah.iloc[0]['polygon_id']
fitur_salah = df_test[df_test['polygon_id'] == salah_id][FITUR_COLS].iloc[0]

# Hitung rata-rata nilai spektral kelas mangrove dan water_body pada data uji
mean_mangrove = df_test[df_test['kelas'] == 'mangrove'][FITUR_COLS].mean()
mean_water    = df_test[df_test['kelas'] == 'water_body'][FITUR_COLS].mean()
mean_forest   = df_test[df_test['kelas'] == 'forest'][FITUR_COLS].mean()

df_perbandingan_spektral = pd.DataFrame({
    'Fitur': FITUR_COLS,
    'Poligon 410 (Aktual: mangrove)': fitur_salah.round(3).values,
    'Rata-rata Mangrove Uji': mean_mangrove.round(3).values,
    'Rata-rata Water Body Uji': mean_water.round(3).values,
    'Rata-rata Forest Uji': mean_forest.round(3).values
})

print('\n--- Perbandingan Profil Spektral Poligon 410 terhadap Rata-rata Kelas ---')
print(df_perbandingan_spektral.to_string(index=False))

print('\nProbabilitas Prediksi Ensemble Random Forest untuk Poligon 410:')
for col in [c for c in df_hasil.columns if c.startswith('prob_')]:
    print(f"  - {col}: {df_salah[col].values[0]:.4f}")
```

    === AUDIT SAMPEL SALAH KLASIFIKASI ===
     polygon_id label_asli    kelas     y_pred  prob_mangrove  prob_water_body  luas_m2  n_valid_px
            410      mang8 mangrove water_body          0.095            0.905  1130.46           8
    
    --- Perbandingan Profil Spektral Poligon 410 terhadap Rata-rata Kelas ---
    Fitur  Poligon 410 (Aktual: mangrove)  Rata-rata Mangrove Uji  Rata-rata Water Body Uji  Rata-rata Forest Uji
      B03                         536.120                 447.654                   683.932               507.720
      B04                         444.750                 309.942                   554.641               283.490
      B08                         980.620                2180.539                   761.725              3371.762
      B11                         410.620                 733.491                   556.588              1653.921
     NDVI                           0.269                   0.715                     0.017                 0.844
     NDWI                          -0.191                  -0.624                     0.112                -0.738
     NDBI                          -0.354                  -0.474                    -0.140                -0.341
    
    Probabilitas Prediksi Ensemble Random Forest untuk Poligon 410:
      - prob_built_up: 0.0000
      - prob_farmland: 0.0000
      - prob_forest: 0.0000
      - prob_mangrove: 0.0950
      - prob_water_body: 0.9050
    

#### 3. Penjelasan Fisis dan Spektral Kesalahan Prediksi Poligon 410
Berdasarkan audit di atas:
1. **Identitas Sampel:** Poligon dengan `polygon_id = 410` (label asli `mang8`), luas area $1.130,46\text{ m}^2$ dengan 8 piksel valid.
2. **Perilaku Model:** Random Forest memprediksi poligon ini sebagai **`water_body`** dengan keyakinan probabilitas ensemble sebesar **90,5%** (`prob_water_body = 0.9050`), sedangkan probabilitas kelas aslinya (`mangrove`) hanya **9,5%** (`prob_mangrove = 0.0950`).
3. **Anomali Respons Spektral:**
   - **Reflektansi Inframerah Dekat (B08):** Nilai B08 poligon 410 tercatat hanya **980,62**, jauh di bawah rata-rata vegetasi mangrove normal (**2.180,54**) maupun hutan (**3.371,76**), dan mendekati nilai air (**761,73**). Kanopi vegetasi yang sehat memantulkan radiasi NIR secara kuat akibat struktur mesofil daun; penurunan drastis pada B08 mengindikasikan ketiadaan kanopi rapat.
   - **Indeks Vegetasi (NDVI):** Nilai NDVI poligon 410 hanya **0,2691**, jauh di bawah ambang batas vegetasi mangrove rapat (rata-rata **0,7150**), dan mendekati karakteristik perairan dangkal/sedimen (rata-rata **0,0167**).
   - **Indeks Air (NDWI):** Nilai NDWI tercatat **-0,1912**, jauh lebih tinggi (lebih basah) dibandingkan mangrove daratan (-0,6244).
   - **Reflektansi SWIR (B11):** Nilai B11 relatif rendah (**410,62**) akibat penyerapan radiasi inframerah gelombang pendek yang kuat oleh molekul air.
4. **Penyebab Biofisik dan Geomorfologis:** Poligon `mang8` terletak pada zona intertidal pesisir Teluk Pangpang. Pada saat satelit Sentinel-2 melintas, kemungkinan besar poligon ini berada dalam kondisi **tergenang pasang laut (*tidal inundation*)** atau memiliki **kerapatan tajuk mangrove yang sangat jarang (*fringe/sparse mangrove*)** dengan substrat lumpur berair. Dominasi reflektansi latar belakang air (*water background reflectance*) menenggelamkan sinyal vegetasi mangrove, sehingga piksel komposit median secara objektif memancarkan karakteristik spektral badan air.

### 5.4 Interpretasi dan Keterbatasan Model

Meskipun model menghasilkan akurasi evaluasi sebesar 99,34% pada data uji, capaian ini harus diinterpretasikan secara kritis. Angka akurasi tinggi tidak serta merta membuktikan bahwa model siap diterapkan secara universal di seluruh wilayah tanpa memahami batasan metodologis berikut:

#### 1. Potensi Kemiripan Spasial (*Spatial Autocorrelation*)
Pemisahan dataset pada Bab 3 telah dilakukan pada level poligon (*polygon-level split*), sehingga tidak ada piksel dari poligon yang sama yang terbagi ke dalam data latih dan uji secara bersamaan. Namun, seluruh poligon acuan dikumpulkan dari kawasan geografis lokal yang terkonsentrasi di Muncar, Teluk Pangpang, dan Tegaldlimo, Banyuwangi. Sesuai Hukum Pertama Geografi Tobler (*everything is related to everything else, but near things are more related than distant things*), poligon uji yang berdekatan secara spasial dengan poligon latih memiliki kemiripan atmosferik, kelembapan tanah, dan variasi musiman yang tinggi. Kemiripan spasial ini berpotensi memberikan estimasi performa yang optimistik (*optimistic performance estimate*).

#### 2. Resolusi Spasial Raster 20 Meter dan Risiko *Mixed Pixel*
Proses pemodelan mengintegrasikan band Sentinel-2 beresolusi 10 meter (B03, B04, B08) dan band beresolusi 20 meter (B11) yang diresample ke dalam satu grid raster 20 meter ($400\text{ m}^2$ per piksel). Pada bentang lahan heterogen, khususnya kawasan pemukiman padat (`built_up`) dan petak sawah sempit (`farmland`), satu piksel sering kali memuat campuran berbagai objek (atap, aspal, pohon perkarangan, pematang, dan air saluran). Bab 3.4 mencatat 104 poligon berukuran kurang dari $400\text{ m}^2$. Fenomena *mixed pixel* ini menyebabkan nilai reflektansi piksel merupakan rata-rata spektral campuran, yang dapat mengaburkan batas kelas pada skala pemetaan operasional yang lebih rinci.

#### 3. Dampak Penggunaan `all_touched=True` pada Ekstraksi Sampel
Pada tahap ekstraksi fitur (Bab 3.4), raster diolah menggunakan parameter `all_touched=True` agar poligon-poligon berukuran kecil tetap dapat mengekstrak piksel raster. Namun, parameter ini memiliki konsekuensi metodologis: setiap piksel yang tepinya sedikit saja bersinggungan dengan poligon akan disertakan dalam perhitungan statistik. Hal ini menyebabkan piksel tepian (*edge/boundary pixels*) yang sebagian besar areanya berada di luar batas poligon ikut memengaruhi nilai fitur rata-rata poligon, sehingga meningkatkan risiko kontaminasi spektral dari tutupan lahan di sekitarnya.

#### 4. Keterbatasan Generalisasi Wilayah (Banyuwangi vs Seluruh Jawa Timur)
Data sampel dikumpulkan secara eksklusif dari lanskap pesisir dan dataran rendah Kabupaten Banyuwangi. Karakteristik biofisik wilayah ini tidak mencerminkan keberagaman spektral Provinsi Jawa Timur secara keseluruhan:
- **Kondisi Topografi & Elevasi:** Model belum pernah dilatih pada vegetasi dataran tinggi pegunungan vulkanik (misalnya kawasan Taman Nasional Bromo Tengger Semeru atau Gunung Ijen) yang memiliki tutupan awan, bayangan lereng (*terrain shadow*), dan jenis tegakan hutan yang berbeda.
- **Tipe Tanah & Iklim:** Wilayah kering karst di Madura atau Pegunungan Sewu di selatan Pacitan memiliki respons reflektansi tanah terbuka dan pertanian lahan kering yang berbeda nyata dengan pertanian irigasi Banyuwangi.
- **Kepadatan Perkotaan:** Karakteristik `built_up` perdesaan Muncar berbeda signifikan dengan kawasan megapolitan Surabaya Raya yang didominasi beton padat dan gedung bertingkat.

Oleh karena itu, **model tidak dapat disimpulkan mampu menggeneralisasi dengan akurasi 99,34% ke wilayah Jawa Timur lainnya** tanpa penambahan sampel referensi baru dari berbagai zona ekoregion.

#### 5. Batas Interpretasi *Feature Importance* dan Skor Evaluasi
Analisis *feature importance* pada Bab 4 didasarkan pada *Mean Decrease Impurity* (MDI) yang dihasilkan oleh pohon Random Forest:
- MDI memiliki kecenderungan bias terhadap fitur kontinu dengan rentang nilai luas, serta membagi skor kepentingan secara acak di antara fitur-fitur yang berkorelasi tinggi (seperti B08, NDVI, dan NDWI).
- Posisi B11 sebagai fitur teratas mengindikasikan peran vital band SWIR dalam memisahkan kelembapan air dan kekeringan lahan terbangun, namun tidak boleh diartikan sebagai hubungan kausalitas ekologis mutlak.
- Skor evaluasi 99,34% adalah performa pada sampel poligon acuan yang bersih dan terisolasi, bukan jaminan bahwa pemetaan menyeluruh secara piksel-ke-piksel (*wall-to-wall mapping*) di seluruh lanskap bebas dari kesalahan klasifikasi.

## 6. Deployment

Tahap *Deployment* merupakan tahap akhir dalam metodologi CRISP-DM. Pada tahap ini, model klasifikasi tutupan lahan Random Forest yang telah dibangun dan dievaluasi diimplementasikan ke dalam aplikasi berbasis web menggunakan Streamlit.

Aplikasi dikembangkan untuk memungkinkan pengguna melakukan klasifikasi terhadap citra Sentinel-2 dalam format GeoTIFF tanpa harus menjalankan kembali seluruh proses pemodelan di dalam notebook. Model Random Forest yang telah dilatih disimpan dalam format `.pkl` dan dimuat oleh aplikasi untuk menghasilkan prediksi tutupan lahan.

### 6.1 Implementasi Aplikasi

Aplikasi menerima masukan berupa citra Sentinel-2 multispektral dalam format GeoTIFF. Selanjutnya, aplikasi menyiapkan tujuh fitur yang digunakan saat pelatihan model, yaitu B03, B04, B08, B11, NDVI, NDWI, dan NDBI. Fitur tersebut diberikan kepada model Random Forest untuk memprediksi kelas tutupan lahan pada setiap piksel valid.

Hasil prediksi disajikan dalam bentuk peta klasifikasi interaktif dengan lima kelas, yaitu lahan terbangun (*built_up*), lahan pertanian (*farmland*), badan air (*water_body*), hutan (*forest*), dan hutan mangrove (*mangrove*). Setiap kelas ditampilkan sebagai layer terpisah sehingga pengguna dapat mengaktifkan atau menonaktifkan kelas tertentu pada peta.

Aplikasi juga menyediakan tabel statistik yang berisi jumlah piksel, estimasi luas wilayah, dan persentase setiap kelas. Hasil klasifikasi dapat diunduh dalam format GeoTIFF, sedangkan ringkasan statistik tersedia dalam format CSV.

### 6.2 Alur Penggunaan Aplikasi

Alur penggunaan aplikasi terdiri atas tahapan berikut:

1. Pengguna mengunggah citra Sentinel-2 dalam format GeoTIFF.
2. Aplikasi membaca data raster dan menyiapkan fitur sesuai dengan model yang telah dilatih.
3. Model Random Forest melakukan prediksi kelas tutupan lahan pada piksel valid.
4. Hasil klasifikasi ditampilkan sebagai peta interaktif dengan layer untuk setiap kelas.
5. Aplikasi menghitung statistik luas dan persentase kelas serta menyediakan fasilitas unduhan hasil.

### 6.3 Teknologi Deployment

Teknologi yang digunakan dalam implementasi aplikasi meliputi Streamlit untuk antarmuka web, scikit-learn untuk model Random Forest, Rasterio untuk pemrosesan GeoTIFF, Folium untuk visualisasi peta interaktif, serta Pandas dan NumPy untuk pengolahan data dan perhitungan statistik.

Aplikasi dipublikasikan menggunakan Streamlit Community Cloud dengan kode aplikasi dan dependensi yang disimpan dalam repository GitHub.

**URL aplikasi:** [Masukkan URL Streamlit setelah deployment berhasil]

### 6.4 Dokumentasi Hasil Deployment

Setelah proses deployment berhasil, dokumentasi dilengkapi dengan tangkapan layar antarmuka aplikasi, hasil klasifikasi pada peta interaktif, tabel statistik tutupan lahan, dan tautan aplikasi yang dapat diakses melalui browser.

Implementasi ini menjadi bentuk penerapan model Random Forest ke dalam aplikasi yang dapat digunakan untuk mengunggah citra, melakukan klasifikasi, mengeksplorasi sebaran kelas secara spasial, dan mengunduh hasil pemodelan.
