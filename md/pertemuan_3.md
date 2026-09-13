# Analisis Time Series Karbon Monoksida (CO) Tingkat Kecamatan di Kota Surabaya Menggunakan TSFEL

## Contents

1. Business Understanding
2. Data Understanding
3. Menentukan Area of Interest (AOI) Tingkat Kecamatan
4. Pengambilan Data CO
5. Eksplorasi Data
6. Data Preprocessing
   - Missing Value
   - Imputation
   - Identifikasi Outlier
   - Perbaikan Outlier
7. Ekstraksi Fitur Menggunakan TSFEL
8. Analisis 68 Fitur
9. Analisis Kemiripan CO dan CO₂
10. Kesimpulan

## 1. Business Understanding

### Latar Belakang

Kualitas udara merupakan salah satu aspek penting dalam lingkungan perkotaan. Salah satu polutan yang dapat digunakan untuk mengamati kondisi kualitas udara adalah Karbon Monoksida (CO), yaitu gas yang dihasilkan dari proses pembakaran tidak sempurna.

Pada analisis ini, data CO di wilayah Kota Surabaya akan dianalisis dengan lingkup wilayah yang lebih kecil, yaitu tingkat kecamatan. Data CO selama 365 hari akan melalui proses preprocessing dan selanjutnya digunakan untuk ekstraksi fitur menggunakan Time Series Feature Extraction Library (TSFEL).

### Tujuan

Analisis ini bertujuan untuk:

1. Mengolah data CO pada tingkat kecamatan di Kota Surabaya selama 365 hari.
2. Menangani missing value menggunakan teknik imputation.
3. Mengidentifikasi dan memperbaiki outlier.
4. Mengekstraksi fitur time series menggunakan TSFEL.
5. Memahami fitur-fitur yang dihasilkan oleh TSFEL.

## 2. Data Understanding

Data yang digunakan berasal dari satelit Sentinel-5P melalui layanan openEO pada Copernicus Data Space Ecosystem. Data mencakup wilayah Kota Surabaya, Jawa Timur, dengan periode pengamatan 24 Agustus 2025 sampai 24 Agustus 2026.

Pada tugas ini, analisis difokuskan pada polutan Karbon Monoksida (CO) dengan lingkup wilayah tingkat kecamatan. Data CO akan diagregasi menjadi data harian dan ditargetkan sebanyak 365 hari untuk selanjutnya digunakan dalam proses preprocessing dan ekstraksi fitur menggunakan TSFEL.


```python
import openeo

print("Library openEO berhasil diimpor.")
```

    Library openEO berhasil diimpor.
    


```python
connection = openeo.connect(
    "https://openeo.dataspace.copernicus.eu"
).authenticate_oidc()

print("Berhasil terhubung ke Copernicus Data Space.")
```

    Authenticated using refresh token.
    Berhasil terhubung ke Copernicus Data Space.
    

## 3. Menentukan Area of Interest (AOI) Tingkat Kecamatan

Batas wilayah kecamatan diperoleh dari dataset Peta Batas Administrasi Kecamatan Tahun 2026 yang disediakan oleh Pemerintah Kota Surabaya. Dataset tersebut berisi 31 wilayah kecamatan dalam format Shapefile (SHP).

Pada analisis ini digunakan Kecamatan Gubeng sebagai Area of Interest (AOI). Batas administrasi kecamatan digunakan sebagai wilayah spasial dalam proses pengambilan data Karbon Monoksida (CO) dari Sentinel-5P.


```python
import geopandas as gpd

gdf_kecamatan = gpd.read_file(
    r"C:\Users\Alif\ProyekSainsData\data\raw\11032026_batas_kec\11032026_BATAS_KEC.shp"
)

gdf_kecamatan.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OBJECTID_1</th>
      <th>OBJECTID</th>
      <th>K</th>
      <th>KODE</th>
      <th>LUAS_KM</th>
      <th>LUAS_HA</th>
      <th>Keterangan</th>
      <th>Shape_Leng</th>
      <th>Shape_Le_1</th>
      <th>Shape_Area</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>BULAK</td>
      <td>35.78.29</td>
      <td>6.23632996142359</td>
      <td>623.632996142359</td>
      <td>Peraturan Walikota Surabaya Nomor 26 Tahun 2023</td>
      <td>27611.996624</td>
      <td>27611.996497</td>
      <td>6.645735e+06</td>
      <td>POLYGON ((696580.441 9202784.509, 696580.458 9...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>2</td>
      <td>WONOKROMO</td>
      <td>35.78.04</td>
      <td>8.27681200407028</td>
      <td>827.681200407028</td>
      <td>Peraturan Walikota Surabaya Nomor 63 Tahun 2022</td>
      <td>19434.690895</td>
      <td>19434.690730</td>
      <td>8.276812e+06</td>
      <td>POLYGON ((692927.102 9193805.435, 692915.698 9...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>3</td>
      <td>TAMBAKSARI</td>
      <td>35.78.10</td>
      <td>8.96572590847566</td>
      <td>896.572590847566</td>
      <td>Peraturan Walikota Surabaya Nomor 63 Tahun 2022</td>
      <td>18585.703899</td>
      <td>18585.703957</td>
      <td>8.965726e+06</td>
      <td>POLYGON ((696506.404 9200045.4, 696503.878 920...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>4</td>
      <td>GENTENG</td>
      <td>35.78.07</td>
      <td>4.09193344170742</td>
      <td>409.193344170742</td>
      <td>Peraturan Walikota Surabaya Nomor 63 Tahun 2022</td>
      <td>12597.494711</td>
      <td>12597.494563</td>
      <td>4.091933e+06</td>
      <td>POLYGON ((693581.28 9198457.402, 693579.957 91...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>5</td>
      <td>BUBUTAN</td>
      <td>35.78.13</td>
      <td>3.90599212881899</td>
      <td>390.599212881899</td>
      <td>Peraturan Walikota Surabaya Nomor 63 Tahun 2022</td>
      <td>9893.936576</td>
      <td>9893.936447</td>
      <td>3.905992e+06</td>
      <td>POLYGON ((691947.224 9198786.6, 691974.783 919...</td>
    </tr>
  </tbody>
</table>
</div>




```python
aoi_gubeng = gdf_kecamatan[
    gdf_kecamatan["K"].str.upper() == "GUBENG"
].copy()

aoi_gubeng
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OBJECTID_1</th>
      <th>OBJECTID</th>
      <th>K</th>
      <th>KODE</th>
      <th>LUAS_KM</th>
      <th>LUAS_HA</th>
      <th>Keterangan</th>
      <th>Shape_Leng</th>
      <th>Shape_Le_1</th>
      <th>Shape_Area</th>
      <th>geometry</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>5</th>
      <td>6</td>
      <td>6</td>
      <td>GUBENG</td>
      <td>35.78.08</td>
      <td>7.92909241371792</td>
      <td>792.909241371792</td>
      <td>Peraturan Walikota Surabaya Nomor 63 Tahun 2022</td>
      <td>17655.597655</td>
      <td>17655.597549</td>
      <td>7.929092e+06</td>
      <td>POLYGON ((694814.169 9196813.503, 694814.429 9...</td>
    </tr>
  </tbody>
</table>
</div>




```python
import matplotlib.pyplot as plt

aoi_gubeng.plot(
    figsize=(8, 8),
    edgecolor="black"
)

plt.title("Area of Interest (AOI) Kecamatan Gubeng")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
```


    
![png](../img/6_output_9_0.png)




```python
aoi_wgs84 = aoi_gubeng.to_crs("EPSG:4326")

aoi = aoi_wgs84.__geo_interface__
```

## 4. Pengambilan Data Karbon Monoksida (CO)

Data Karbon Monoksida (CO) diambil dari koleksi Sentinel-5P L2 menggunakan layanan openEO pada Copernicus Data Space Ecosystem. Periode pengambilan data ditetapkan dari 24 Agustus 2025 sampai 24 Agustus 2026.

Data CO kemudian diagregasi berdasarkan waktu menjadi data harian dan berdasarkan wilayah menggunakan Area of Interest (AOI) Kecamatan Gubeng.

Hasil pengambilan data menunjukkan bahwa tidak seluruh hari dalam periode tersebut memiliki observasi. Data yang tersedia berjumlah 197 hari, dengan observasi terakhir tersedia pada 22 Agustus 2026. Untuk keperluan analisis time series selama 365 hari, rentang tanggal lengkap kemudian dibentuk dan tanggal yang tidak memiliki observasi ditandai sebagai missing value sebelum dilakukan tahap preprocessing.


```python
polutan = "CO"

temporal_extent = [
    "2025-08-24",
    "2026-08-24"
]
```


```python
datacube_co = connection.load_collection(
    "SENTINEL_5P_L2",
    temporal_extent=temporal_extent,
    spatial_extent={
        "west": aoi_wgs84.total_bounds[0],
        "south": aoi_wgs84.total_bounds[1],
        "east": aoi_wgs84.total_bounds[2],
        "north": aoi_wgs84.total_bounds[3]
    },
    bands=[polutan]
)
```


```python
datacube_co = datacube_co.aggregate_temporal_period(
    reducer="mean",
    period="day"
)
```


```python
datacube_co = datacube_co.aggregate_spatial(
    reducer="mean",
    geometries=aoi
)
```


```python
output_file = "kualitas_udara_CO_Gubeng.nc"

print("Mengeksekusi unduhan data CO...")

datacube_co.execute_batch(
    title="Analisis CO Kecamatan Gubeng",
    outputfile=output_file
)

print(f"Data CO berhasil disimpan sebagai {output_file}")
```

    Mengeksekusi unduhan data CO...
    0:00:00 Job 'j-26091305592545cc8b39d0511df58494': send 'start'
    0:00:03 Job 'j-26091305592545cc8b39d0511df58494': queued (progress 0%)
    0:00:09 Job 'j-26091305592545cc8b39d0511df58494': queued (progress 0%)
    0:00:15 Job 'j-26091305592545cc8b39d0511df58494': queued (progress 0%)
    0:00:24 Job 'j-26091305592545cc8b39d0511df58494': queued (progress 0%)
    0:00:35 Job 'j-26091305592545cc8b39d0511df58494': queued (progress 0%)
    0:00:47 Job 'j-26091305592545cc8b39d0511df58494': running (progress N/A)
    0:01:03 Job 'j-26091305592545cc8b39d0511df58494': running (progress N/A)
    0:01:23 Job 'j-26091305592545cc8b39d0511df58494': running (progress N/A)
    0:01:47 Job 'j-26091305592545cc8b39d0511df58494': running (progress N/A)
    0:02:18 Job 'j-26091305592545cc8b39d0511df58494': running (progress N/A)
    0:02:55 Job 'j-26091305592545cc8b39d0511df58494': running (progress N/A)
    0:03:43 Job 'j-26091305592545cc8b39d0511df58494': finished (progress 100%)
    Data CO berhasil disimpan sebagai kualitas_udara_CO_Gubeng.nc
    


```python
import xarray as xr
import pandas as pd

# Membaca hasil ekstraksi data CO
ds_co = xr.open_dataset(
    "ProyekSainsData/data/raw/kualitas_udara_CO_Gubeng.nc"
)

# Menampilkan struktur dataset hasil ekstraksi
ds_co
```




<div><svg style="position: absolute; width: 0; height: 0; overflow: hidden">
<defs>
<symbol id="icon-database" viewBox="0 0 32 32">
<path d="M16 0c-8.837 0-16 2.239-16 5v4c0 2.761 7.163 5 16 5s16-2.239 16-5v-4c0-2.761-7.163-5-16-5z"></path>
<path d="M16 17c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
<path d="M16 26c-8.837 0-16-2.239-16-5v6c0 2.761 7.163 5 16 5s16-2.239 16-5v-6c0 2.761-7.163 5-16 5z"></path>
</symbol>
<symbol id="icon-file-text2" viewBox="0 0 32 32">
<path d="M28.681 7.159c-0.694-0.947-1.662-2.053-2.724-3.116s-2.169-2.030-3.116-2.724c-1.612-1.182-2.393-1.319-2.841-1.319h-15.5c-1.378 0-2.5 1.121-2.5 2.5v27c0 1.378 1.122 2.5 2.5 2.5h23c1.378 0 2.5-1.122 2.5-2.5v-19.5c0-0.448-0.137-1.23-1.319-2.841zM24.543 5.457c0.959 0.959 1.712 1.825 2.268 2.543h-4.811v-4.811c0.718 0.556 1.584 1.309 2.543 2.268zM28 29.5c0 0.271-0.229 0.5-0.5 0.5h-23c-0.271 0-0.5-0.229-0.5-0.5v-27c0-0.271 0.229-0.5 0.5-0.5 0 0 15.499-0 15.5 0v7c0 0.552 0.448 1 1 1h7v19.5z"></path>
<path d="M23 26h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 22h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
<path d="M23 18h-14c-0.552 0-1-0.448-1-1s0.448-1 1-1h14c0.552 0 1 0.448 1 1s-0.448 1-1 1z"></path>
</symbol>
</defs>
</svg>
<style>/* CSS stylesheet for displaying xarray objects in jupyterlab.
 *
 */

:root {
  --xr-font-color0: var(--jp-content-font-color0, rgba(0, 0, 0, 1));
  --xr-font-color2: var(--jp-content-font-color2, rgba(0, 0, 0, 0.54));
  --xr-font-color3: var(--jp-content-font-color3, rgba(0, 0, 0, 0.38));
  --xr-border-color: var(--jp-border-color2, #e0e0e0);
  --xr-disabled-color: var(--jp-layout-color3, #bdbdbd);
  --xr-background-color: var(--jp-layout-color0, white);
  --xr-background-color-row-even: var(--jp-layout-color1, white);
  --xr-background-color-row-odd: var(--jp-layout-color2, #eeeeee);
}

html[theme="dark"],
html[data-theme="dark"],
body[data-theme="dark"],
body.vscode-dark {
  --xr-font-color0: rgba(255, 255, 255, 1);
  --xr-font-color2: rgba(255, 255, 255, 0.54);
  --xr-font-color3: rgba(255, 255, 255, 0.38);
  --xr-border-color: #1f1f1f;
  --xr-disabled-color: #515151;
  --xr-background-color: #111111;
  --xr-background-color-row-even: #111111;
  --xr-background-color-row-odd: #313131;
}

.xr-wrap {
  display: block !important;
  min-width: 300px;
  max-width: 700px;
}

.xr-text-repr-fallback {
  /* fallback to plain text repr when CSS is not injected (untrusted notebook) */
  display: none;
}

.xr-header {
  padding-top: 6px;
  padding-bottom: 6px;
  margin-bottom: 4px;
  border-bottom: solid 1px var(--xr-border-color);
}

.xr-header > div,
.xr-header > ul {
  display: inline;
  margin-top: 0;
  margin-bottom: 0;
}

.xr-obj-type,
.xr-array-name {
  margin-left: 2px;
  margin-right: 10px;
}

.xr-obj-type {
  color: var(--xr-font-color2);
}

.xr-sections {
  padding-left: 0 !important;
  display: grid;
  grid-template-columns: 150px auto auto 1fr 0 20px 0 20px;
}

.xr-section-item {
  display: contents;
}

.xr-section-item input {
  display: inline-block;
  opacity: 0;
  height: 0;
}

.xr-section-item input + label {
  color: var(--xr-disabled-color);
}

.xr-section-item input:enabled + label {
  cursor: pointer;
  color: var(--xr-font-color2);
}

.xr-section-item input:focus + label {
  border: 2px solid var(--xr-font-color0);
}

.xr-section-item input:enabled + label:hover {
  color: var(--xr-font-color0);
}

.xr-section-summary {
  grid-column: 1;
  color: var(--xr-font-color2);
  font-weight: 500;
}

.xr-section-summary > span {
  display: inline-block;
  padding-left: 0.5em;
}

.xr-section-summary-in:disabled + label {
  color: var(--xr-font-color2);
}

.xr-section-summary-in + label:before {
  display: inline-block;
  content: "►";
  font-size: 11px;
  width: 15px;
  text-align: center;
}

.xr-section-summary-in:disabled + label:before {
  color: var(--xr-disabled-color);
}

.xr-section-summary-in:checked + label:before {
  content: "▼";
}

.xr-section-summary-in:checked + label > span {
  display: none;
}

.xr-section-summary,
.xr-section-inline-details {
  padding-top: 4px;
  padding-bottom: 4px;
}

.xr-section-inline-details {
  grid-column: 2 / -1;
}

.xr-section-details {
  display: none;
  grid-column: 1 / -1;
  margin-bottom: 5px;
}

.xr-section-summary-in:checked ~ .xr-section-details {
  display: contents;
}

.xr-array-wrap {
  grid-column: 1 / -1;
  display: grid;
  grid-template-columns: 20px auto;
}

.xr-array-wrap > label {
  grid-column: 1;
  vertical-align: top;
}

.xr-preview {
  color: var(--xr-font-color3);
}

.xr-array-preview,
.xr-array-data {
  padding: 0 5px !important;
  grid-column: 2;
}

.xr-array-data,
.xr-array-in:checked ~ .xr-array-preview {
  display: none;
}

.xr-array-in:checked ~ .xr-array-data,
.xr-array-preview {
  display: inline-block;
}

.xr-dim-list {
  display: inline-block !important;
  list-style: none;
  padding: 0 !important;
  margin: 0;
}

.xr-dim-list li {
  display: inline-block;
  padding: 0;
  margin: 0;
}

.xr-dim-list:before {
  content: "(";
}

.xr-dim-list:after {
  content: ")";
}

.xr-dim-list li:not(:last-child):after {
  content: ",";
  padding-right: 5px;
}

.xr-has-index {
  font-weight: bold;
}

.xr-var-list,
.xr-var-item {
  display: contents;
}

.xr-var-item > div,
.xr-var-item label,
.xr-var-item > .xr-var-name span {
  background-color: var(--xr-background-color-row-even);
  margin-bottom: 0;
}

.xr-var-item > .xr-var-name:hover span {
  padding-right: 5px;
}

.xr-var-list > li:nth-child(odd) > div,
.xr-var-list > li:nth-child(odd) > label,
.xr-var-list > li:nth-child(odd) > .xr-var-name span {
  background-color: var(--xr-background-color-row-odd);
}

.xr-var-name {
  grid-column: 1;
}

.xr-var-dims {
  grid-column: 2;
}

.xr-var-dtype {
  grid-column: 3;
  text-align: right;
  color: var(--xr-font-color2);
}

.xr-var-preview {
  grid-column: 4;
}

.xr-index-preview {
  grid-column: 2 / 5;
  color: var(--xr-font-color2);
}

.xr-var-name,
.xr-var-dims,
.xr-var-dtype,
.xr-preview,
.xr-attrs dt {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: 10px;
}

.xr-var-name:hover,
.xr-var-dims:hover,
.xr-var-dtype:hover,
.xr-attrs dt:hover {
  overflow: visible;
  width: auto;
  z-index: 1;
}

.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  display: none;
  background-color: var(--xr-background-color) !important;
  padding-bottom: 5px !important;
}

.xr-var-attrs-in:checked ~ .xr-var-attrs,
.xr-var-data-in:checked ~ .xr-var-data,
.xr-index-data-in:checked ~ .xr-index-data {
  display: block;
}

.xr-var-data > table {
  float: right;
}

.xr-var-name span,
.xr-var-data,
.xr-index-name div,
.xr-index-data,
.xr-attrs {
  padding-left: 25px !important;
}

.xr-attrs,
.xr-var-attrs,
.xr-var-data,
.xr-index-data {
  grid-column: 1 / -1;
}

dl.xr-attrs {
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 125px auto;
}

.xr-attrs dt,
.xr-attrs dd {
  padding: 0;
  margin: 0;
  float: left;
  padding-right: 10px;
  width: auto;
}

.xr-attrs dt {
  font-weight: normal;
  grid-column: 1;
}

.xr-attrs dt:hover span {
  display: inline-block;
  background: var(--xr-background-color);
  padding-right: 10px;
}

.xr-attrs dd {
  grid-column: 2;
  white-space: pre-wrap;
  word-break: break-all;
}

.xr-icon-database,
.xr-icon-file-text2,
.xr-no-icon {
  display: inline-block;
  vertical-align: middle;
  width: 1em;
  height: 1.5em !important;
  stroke-width: 0;
  stroke: currentColor;
  fill: currentColor;
}
</style><pre class='xr-text-repr-fallback'>&lt;xarray.Dataset&gt; Size: 3kB
Dimensions:        (t: 197, feature: 1)
Coordinates:
  * t              (t) datetime64[ns] 2kB 2025-08-24 2025-08-25 ... 2026-08-22
    lat            (feature) float64 8B ...
    lon            (feature) float64 8B ...
    feature_names  (feature) &lt;U9 36B ...
Dimensions without coordinates: feature
Data variables:
    CO             (feature, t) float64 2kB ...
Attributes:
    Conventions:  CF-1.8
    source:       Aggregated timeseries generated by openEO GeoPySpark backend.</pre><div class='xr-wrap' style='display:none'><div class='xr-header'><div class='xr-obj-type'>xarray.Dataset</div></div><ul class='xr-sections'><li class='xr-section-item'><input id='section-44599861-805a-4288-b9d3-35edc22692ad' class='xr-section-summary-in' type='checkbox' disabled ><label for='section-44599861-805a-4288-b9d3-35edc22692ad' class='xr-section-summary'  title='Expand/collapse section'>Dimensions:</label><div class='xr-section-inline-details'><ul class='xr-dim-list'><li><span class='xr-has-index'>t</span>: 197</li><li><span>feature</span>: 1</li></ul></div><div class='xr-section-details'></div></li><li class='xr-section-item'><input id='section-4449d89c-509d-4850-99e0-03a526481890' class='xr-section-summary-in' type='checkbox'  checked><label for='section-4449d89c-509d-4850-99e0-03a526481890' class='xr-section-summary' >Coordinates: <span>(4)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span class='xr-has-index'>t</span></div><div class='xr-var-dims'>(t)</div><div class='xr-var-dtype'>datetime64[ns]</div><div class='xr-var-preview xr-preview'>2025-08-24 ... 2026-08-22</div><input id='attrs-cc8e31ad-6f88-4e0d-85f9-8e707af607ea' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-cc8e31ad-6f88-4e0d-85f9-8e707af607ea' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-71dde49b-2bf0-4fb3-b916-532de7631c31' class='xr-var-data-in' type='checkbox'><label for='data-71dde49b-2bf0-4fb3-b916-532de7631c31' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>standard_name :</span></dt><dd>time</dd></dl></div><div class='xr-var-data'><pre>array([&#x27;2025-08-24T00:00:00.000000000&#x27;, &#x27;2025-08-25T00:00:00.000000000&#x27;,
       &#x27;2025-08-28T00:00:00.000000000&#x27;, &#x27;2025-08-29T00:00:00.000000000&#x27;,
       &#x27;2025-08-30T00:00:00.000000000&#x27;, &#x27;2025-09-03T00:00:00.000000000&#x27;,
       &#x27;2025-09-04T00:00:00.000000000&#x27;, &#x27;2025-09-05T00:00:00.000000000&#x27;,
       &#x27;2025-09-07T00:00:00.000000000&#x27;, &#x27;2025-09-09T00:00:00.000000000&#x27;,
       &#x27;2025-09-12T00:00:00.000000000&#x27;, &#x27;2025-09-13T00:00:00.000000000&#x27;,
       &#x27;2025-09-14T00:00:00.000000000&#x27;, &#x27;2025-09-15T00:00:00.000000000&#x27;,
       &#x27;2025-09-19T00:00:00.000000000&#x27;, &#x27;2025-09-20T00:00:00.000000000&#x27;,
       &#x27;2025-09-21T00:00:00.000000000&#x27;, &#x27;2025-09-22T00:00:00.000000000&#x27;,
       &#x27;2025-09-23T00:00:00.000000000&#x27;, &#x27;2025-09-25T00:00:00.000000000&#x27;,
       &#x27;2025-09-27T00:00:00.000000000&#x27;, &#x27;2025-09-28T00:00:00.000000000&#x27;,
       &#x27;2025-09-29T00:00:00.000000000&#x27;, &#x27;2025-10-03T00:00:00.000000000&#x27;,
       &#x27;2025-10-04T00:00:00.000000000&#x27;, &#x27;2025-10-05T00:00:00.000000000&#x27;,
       &#x27;2025-10-06T00:00:00.000000000&#x27;, &#x27;2025-10-07T00:00:00.000000000&#x27;,
       &#x27;2025-10-09T00:00:00.000000000&#x27;, &#x27;2025-10-10T00:00:00.000000000&#x27;,
       &#x27;2025-10-11T00:00:00.000000000&#x27;, &#x27;2025-10-12T00:00:00.000000000&#x27;,
       &#x27;2025-10-14T00:00:00.000000000&#x27;, &#x27;2025-10-15T00:00:00.000000000&#x27;,
       &#x27;2025-10-16T00:00:00.000000000&#x27;, &#x27;2025-10-17T00:00:00.000000000&#x27;,
       &#x27;2025-10-26T00:00:00.000000000&#x27;, &#x27;2025-10-28T00:00:00.000000000&#x27;,
       &#x27;2025-11-06T00:00:00.000000000&#x27;, &#x27;2025-11-07T00:00:00.000000000&#x27;,
       &#x27;2025-11-23T00:00:00.000000000&#x27;, &#x27;2025-11-26T00:00:00.000000000&#x27;,
       &#x27;2025-11-28T00:00:00.000000000&#x27;, &#x27;2025-12-03T00:00:00.000000000&#x27;,
       &#x27;2025-12-05T00:00:00.000000000&#x27;, &#x27;2025-12-10T00:00:00.000000000&#x27;,
       &#x27;2025-12-11T00:00:00.000000000&#x27;, &#x27;2025-12-12T00:00:00.000000000&#x27;,
       &#x27;2025-12-15T00:00:00.000000000&#x27;, &#x27;2025-12-17T00:00:00.000000000&#x27;,
       &#x27;2025-12-21T00:00:00.000000000&#x27;, &#x27;2025-12-22T00:00:00.000000000&#x27;,
       &#x27;2025-12-23T00:00:00.000000000&#x27;, &#x27;2025-12-25T00:00:00.000000000&#x27;,
       &#x27;2025-12-29T00:00:00.000000000&#x27;, &#x27;2026-01-03T00:00:00.000000000&#x27;,
       &#x27;2026-01-04T00:00:00.000000000&#x27;, &#x27;2026-01-09T00:00:00.000000000&#x27;,
       &#x27;2026-01-14T00:00:00.000000000&#x27;, &#x27;2026-01-19T00:00:00.000000000&#x27;,
       &#x27;2026-01-21T00:00:00.000000000&#x27;, &#x27;2026-01-24T00:00:00.000000000&#x27;,
       &#x27;2026-01-25T00:00:00.000000000&#x27;, &#x27;2026-01-27T00:00:00.000000000&#x27;,
       &#x27;2026-01-29T00:00:00.000000000&#x27;, &#x27;2026-01-30T00:00:00.000000000&#x27;,
       &#x27;2026-01-31T00:00:00.000000000&#x27;, &#x27;2026-02-02T00:00:00.000000000&#x27;,
       &#x27;2026-02-03T00:00:00.000000000&#x27;, &#x27;2026-02-04T00:00:00.000000000&#x27;,
       &#x27;2026-02-06T00:00:00.000000000&#x27;, &#x27;2026-02-16T00:00:00.000000000&#x27;,
       &#x27;2026-02-17T00:00:00.000000000&#x27;, &#x27;2026-02-25T00:00:00.000000000&#x27;,
       &#x27;2026-02-27T00:00:00.000000000&#x27;, &#x27;2026-02-28T00:00:00.000000000&#x27;,
       &#x27;2026-03-05T00:00:00.000000000&#x27;, &#x27;2026-03-08T00:00:00.000000000&#x27;,
       &#x27;2026-03-10T00:00:00.000000000&#x27;, &#x27;2026-03-12T00:00:00.000000000&#x27;,
       &#x27;2026-03-14T00:00:00.000000000&#x27;, &#x27;2026-03-15T00:00:00.000000000&#x27;,
       &#x27;2026-03-16T00:00:00.000000000&#x27;, &#x27;2026-03-17T00:00:00.000000000&#x27;,
       &#x27;2026-03-18T00:00:00.000000000&#x27;, &#x27;2026-03-23T00:00:00.000000000&#x27;,
       &#x27;2026-03-25T00:00:00.000000000&#x27;, &#x27;2026-03-26T00:00:00.000000000&#x27;,
       &#x27;2026-03-27T00:00:00.000000000&#x27;, &#x27;2026-03-29T00:00:00.000000000&#x27;,
       &#x27;2026-04-01T00:00:00.000000000&#x27;, &#x27;2026-04-02T00:00:00.000000000&#x27;,
       &#x27;2026-04-03T00:00:00.000000000&#x27;, &#x27;2026-04-05T00:00:00.000000000&#x27;,
       &#x27;2026-04-11T00:00:00.000000000&#x27;, &#x27;2026-04-13T00:00:00.000000000&#x27;,
       &#x27;2026-04-15T00:00:00.000000000&#x27;, &#x27;2026-04-16T00:00:00.000000000&#x27;,
       &#x27;2026-04-17T00:00:00.000000000&#x27;, &#x27;2026-04-18T00:00:00.000000000&#x27;,
       &#x27;2026-04-19T00:00:00.000000000&#x27;, &#x27;2026-04-21T00:00:00.000000000&#x27;,
       &#x27;2026-04-25T00:00:00.000000000&#x27;, &#x27;2026-04-26T00:00:00.000000000&#x27;,
       &#x27;2026-05-01T00:00:00.000000000&#x27;, &#x27;2026-05-02T00:00:00.000000000&#x27;,
       &#x27;2026-05-03T00:00:00.000000000&#x27;, &#x27;2026-05-05T00:00:00.000000000&#x27;,
       &#x27;2026-05-06T00:00:00.000000000&#x27;, &#x27;2026-05-07T00:00:00.000000000&#x27;,
       &#x27;2026-05-08T00:00:00.000000000&#x27;, &#x27;2026-05-10T00:00:00.000000000&#x27;,
       &#x27;2026-05-11T00:00:00.000000000&#x27;, &#x27;2026-05-12T00:00:00.000000000&#x27;,
       &#x27;2026-05-13T00:00:00.000000000&#x27;, &#x27;2026-05-15T00:00:00.000000000&#x27;,
       &#x27;2026-05-17T00:00:00.000000000&#x27;, &#x27;2026-05-18T00:00:00.000000000&#x27;,
       &#x27;2026-05-19T00:00:00.000000000&#x27;, &#x27;2026-05-21T00:00:00.000000000&#x27;,
       &#x27;2026-05-22T00:00:00.000000000&#x27;, &#x27;2026-05-23T00:00:00.000000000&#x27;,
       &#x27;2026-05-24T00:00:00.000000000&#x27;, &#x27;2026-05-25T00:00:00.000000000&#x27;,
       &#x27;2026-05-26T00:00:00.000000000&#x27;, &#x27;2026-05-27T00:00:00.000000000&#x27;,
       &#x27;2026-05-28T00:00:00.000000000&#x27;, &#x27;2026-05-29T00:00:00.000000000&#x27;,
       &#x27;2026-05-31T00:00:00.000000000&#x27;, &#x27;2026-06-01T00:00:00.000000000&#x27;,
       &#x27;2026-06-02T00:00:00.000000000&#x27;, &#x27;2026-06-03T00:00:00.000000000&#x27;,
       &#x27;2026-06-04T00:00:00.000000000&#x27;, &#x27;2026-06-05T00:00:00.000000000&#x27;,
       &#x27;2026-06-06T00:00:00.000000000&#x27;, &#x27;2026-06-07T00:00:00.000000000&#x27;,
       &#x27;2026-06-08T00:00:00.000000000&#x27;, &#x27;2026-06-09T00:00:00.000000000&#x27;,
       &#x27;2026-06-10T00:00:00.000000000&#x27;, &#x27;2026-06-11T00:00:00.000000000&#x27;,
       &#x27;2026-06-13T00:00:00.000000000&#x27;, &#x27;2026-06-14T00:00:00.000000000&#x27;,
       &#x27;2026-06-15T00:00:00.000000000&#x27;, &#x27;2026-06-17T00:00:00.000000000&#x27;,
       &#x27;2026-06-18T00:00:00.000000000&#x27;, &#x27;2026-06-19T00:00:00.000000000&#x27;,
       &#x27;2026-06-22T00:00:00.000000000&#x27;, &#x27;2026-06-23T00:00:00.000000000&#x27;,
       &#x27;2026-06-24T00:00:00.000000000&#x27;, &#x27;2026-06-25T00:00:00.000000000&#x27;,
       &#x27;2026-06-26T00:00:00.000000000&#x27;, &#x27;2026-06-27T00:00:00.000000000&#x27;,
       &#x27;2026-06-28T00:00:00.000000000&#x27;, &#x27;2026-06-29T00:00:00.000000000&#x27;,
       &#x27;2026-06-30T00:00:00.000000000&#x27;, &#x27;2026-07-01T00:00:00.000000000&#x27;,
       &#x27;2026-07-02T00:00:00.000000000&#x27;, &#x27;2026-07-03T00:00:00.000000000&#x27;,
       &#x27;2026-07-04T00:00:00.000000000&#x27;, &#x27;2026-07-05T00:00:00.000000000&#x27;,
       &#x27;2026-07-06T00:00:00.000000000&#x27;, &#x27;2026-07-08T00:00:00.000000000&#x27;,
       &#x27;2026-07-09T00:00:00.000000000&#x27;, &#x27;2026-07-10T00:00:00.000000000&#x27;,
       &#x27;2026-07-12T00:00:00.000000000&#x27;, &#x27;2026-07-13T00:00:00.000000000&#x27;,
       &#x27;2026-07-14T00:00:00.000000000&#x27;, &#x27;2026-07-15T00:00:00.000000000&#x27;,
       &#x27;2026-07-16T00:00:00.000000000&#x27;, &#x27;2026-07-17T00:00:00.000000000&#x27;,
       &#x27;2026-07-18T00:00:00.000000000&#x27;, &#x27;2026-07-19T00:00:00.000000000&#x27;,
       &#x27;2026-07-20T00:00:00.000000000&#x27;, &#x27;2026-07-21T00:00:00.000000000&#x27;,
       &#x27;2026-07-22T00:00:00.000000000&#x27;, &#x27;2026-07-24T00:00:00.000000000&#x27;,
       &#x27;2026-07-25T00:00:00.000000000&#x27;, &#x27;2026-07-26T00:00:00.000000000&#x27;,
       &#x27;2026-07-29T00:00:00.000000000&#x27;, &#x27;2026-07-31T00:00:00.000000000&#x27;,
       &#x27;2026-08-01T00:00:00.000000000&#x27;, &#x27;2026-08-03T00:00:00.000000000&#x27;,
       &#x27;2026-08-04T00:00:00.000000000&#x27;, &#x27;2026-08-05T00:00:00.000000000&#x27;,
       &#x27;2026-08-06T00:00:00.000000000&#x27;, &#x27;2026-08-07T00:00:00.000000000&#x27;,
       &#x27;2026-08-09T00:00:00.000000000&#x27;, &#x27;2026-08-10T00:00:00.000000000&#x27;,
       &#x27;2026-08-11T00:00:00.000000000&#x27;, &#x27;2026-08-12T00:00:00.000000000&#x27;,
       &#x27;2026-08-13T00:00:00.000000000&#x27;, &#x27;2026-08-14T00:00:00.000000000&#x27;,
       &#x27;2026-08-16T00:00:00.000000000&#x27;, &#x27;2026-08-17T00:00:00.000000000&#x27;,
       &#x27;2026-08-19T00:00:00.000000000&#x27;, &#x27;2026-08-21T00:00:00.000000000&#x27;,
       &#x27;2026-08-22T00:00:00.000000000&#x27;], dtype=&#x27;datetime64[ns]&#x27;)</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lat</span></div><div class='xr-var-dims'>(feature)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-2a0d37b3-45e9-4dc5-badc-4f7501611543' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-2a0d37b3-45e9-4dc5-badc-4f7501611543' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-6a05d6df-8ad5-4b9a-a4b1-af522c39e828' class='xr-var-data-in' type='checkbox'><label for='data-6a05d6df-8ad5-4b9a-a4b1-af522c39e828' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>units :</span></dt><dd>degrees_north</dd><dt><span>standard_name :</span></dt><dd>latitude</dd></dl></div><div class='xr-var-data'><pre>[1 values with dtype=float64]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>lon</span></div><div class='xr-var-dims'>(feature)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-44637148-5cb2-4ff4-b3c0-d018f861b74a' class='xr-var-attrs-in' type='checkbox' ><label for='attrs-44637148-5cb2-4ff4-b3c0-d018f861b74a' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-ebaf88ac-70af-4833-acfe-54b2913df3da' class='xr-var-data-in' type='checkbox'><label for='data-ebaf88ac-70af-4833-acfe-54b2913df3da' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'><dt><span>units :</span></dt><dd>degrees_east</dd><dt><span>standard_name :</span></dt><dd>longitude</dd></dl></div><div class='xr-var-data'><pre>[1 values with dtype=float64]</pre></div></li><li class='xr-var-item'><div class='xr-var-name'><span>feature_names</span></div><div class='xr-var-dims'>(feature)</div><div class='xr-var-dtype'>&lt;U9</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-52f29662-afae-4e02-985d-0120ab030c6d' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-52f29662-afae-4e02-985d-0120ab030c6d' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-4c992f80-2289-47e1-a820-ae6f2a49ebe1' class='xr-var-data-in' type='checkbox'><label for='data-4c992f80-2289-47e1-a820-ae6f2a49ebe1' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>[1 values with dtype=&lt;U9]</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-5f8a177c-3958-4aa0-bac6-8fd3b0cfd276' class='xr-section-summary-in' type='checkbox'  checked><label for='section-5f8a177c-3958-4aa0-bac6-8fd3b0cfd276' class='xr-section-summary' >Data variables: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-var-name'><span>CO</span></div><div class='xr-var-dims'>(feature, t)</div><div class='xr-var-dtype'>float64</div><div class='xr-var-preview xr-preview'>...</div><input id='attrs-ddd19842-338b-4545-86bb-b6589c4aba75' class='xr-var-attrs-in' type='checkbox' disabled><label for='attrs-ddd19842-338b-4545-86bb-b6589c4aba75' title='Show/Hide attributes'><svg class='icon xr-icon-file-text2'><use xlink:href='#icon-file-text2'></use></svg></label><input id='data-83dfa03b-1b3f-458b-ae78-e270b171fd0a' class='xr-var-data-in' type='checkbox'><label for='data-83dfa03b-1b3f-458b-ae78-e270b171fd0a' title='Show/Hide data repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-var-attrs'><dl class='xr-attrs'></dl></div><div class='xr-var-data'><pre>[197 values with dtype=float64]</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-7a370e0a-4700-481d-8319-3335578caed3' class='xr-section-summary-in' type='checkbox'  ><label for='section-7a370e0a-4700-481d-8319-3335578caed3' class='xr-section-summary' >Indexes: <span>(1)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><ul class='xr-var-list'><li class='xr-var-item'><div class='xr-index-name'><div>t</div></div><div class='xr-index-preview'>PandasIndex</div><input type='checkbox' disabled/><label></label><input id='index-32fd626f-9e3c-4ac8-8c4e-f1bbbc93d9b8' class='xr-index-data-in' type='checkbox'/><label for='index-32fd626f-9e3c-4ac8-8c4e-f1bbbc93d9b8' title='Show/Hide index repr'><svg class='icon xr-icon-database'><use xlink:href='#icon-database'></use></svg></label><div class='xr-index-data'><pre>PandasIndex(DatetimeIndex([&#x27;2025-08-24&#x27;, &#x27;2025-08-25&#x27;, &#x27;2025-08-28&#x27;, &#x27;2025-08-29&#x27;,
               &#x27;2025-08-30&#x27;, &#x27;2025-09-03&#x27;, &#x27;2025-09-04&#x27;, &#x27;2025-09-05&#x27;,
               &#x27;2025-09-07&#x27;, &#x27;2025-09-09&#x27;,
               ...
               &#x27;2026-08-10&#x27;, &#x27;2026-08-11&#x27;, &#x27;2026-08-12&#x27;, &#x27;2026-08-13&#x27;,
               &#x27;2026-08-14&#x27;, &#x27;2026-08-16&#x27;, &#x27;2026-08-17&#x27;, &#x27;2026-08-19&#x27;,
               &#x27;2026-08-21&#x27;, &#x27;2026-08-22&#x27;],
              dtype=&#x27;datetime64[ns]&#x27;, name=&#x27;t&#x27;, length=197, freq=None))</pre></div></li></ul></div></li><li class='xr-section-item'><input id='section-f574a650-4b10-4893-8bcd-31c1c1b5fd27' class='xr-section-summary-in' type='checkbox'  checked><label for='section-f574a650-4b10-4893-8bcd-31c1c1b5fd27' class='xr-section-summary' >Attributes: <span>(2)</span></label><div class='xr-section-inline-details'></div><div class='xr-section-details'><dl class='xr-attrs'><dt><span>Conventions :</span></dt><dd>CF-1.8</dd><dt><span>source :</span></dt><dd>Aggregated timeseries generated by openEO GeoPySpark backend.</dd></dl></div></li></ul></div></div>




```python
# Mengubah hasil NetCDF menjadi DataFrame
df_co_raw = ds_co["CO"].to_dataframe().reset_index()

# Mengambil kolom waktu dan nilai CO
df_co_raw = df_co_raw[["t", "CO"]]

# Mengubah nama dan format tanggal
df_co_raw = df_co_raw.rename(columns={"t": "Tanggal"})
df_co_raw["Tanggal"] = pd.to_datetime(df_co_raw["Tanggal"])

# Mengurutkan data berdasarkan tanggal
df_co_raw = df_co_raw.sort_values("Tanggal")

# Membentuk rentang tanggal lengkap selama 365 hari
tanggal_lengkap = pd.date_range(
    start="2025-08-24",
    periods=365,
    freq="D"
)

# Melengkapi tanggal yang tidak tersedia dengan NaN
df_co = (
    df_co_raw
    .set_index("Tanggal")
    .reindex(tanggal_lengkap)
)

df_co.index.name = "Tanggal"
df_co = df_co.reset_index()

# Menyimpan data hasil persiapan
df_co.to_csv(
    "ProyekSainsData/data/processed/kualitas_udara_CO_Gubeng_365hari.csv",
    index=False
)
```

## 5. Eksplorasi Data

Eksplorasi data dilakukan untuk memahami karakteristik awal data Karbon Monoksida (CO) sebelum memasuki tahap preprocessing. Eksplorasi mencakup statistik deskriptif dan visualisasi deret waktu untuk melihat pola perubahan nilai CO serta kondisi data yang belum diproses.


```python
df_co[["CO"]].describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CO</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>197.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>0.028914</td>
    </tr>
    <tr>
      <th>std</th>
      <td>0.004292</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.017851</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.026155</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.028623</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.031243</td>
    </tr>
    <tr>
      <th>max</th>
      <td>0.043366</td>
    </tr>
  </tbody>
</table>
</div>




```python
import matplotlib.pyplot as plt

plt.figure(figsize=(14, 5))

plt.plot(
    df_co["Tanggal"],
    df_co["CO"]
)

plt.title("Time Series Karbon Monoksida (CO) Kecamatan Gubeng")
plt.xlabel("Tanggal")
plt.ylabel("Konsentrasi CO")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```


    
![png](../img/7_output_21_0.png)




```python
ringkasan_missing = pd.DataFrame({
    "Kondisi": [
        "Data tersedia dari Sentinel-5P",
        "Total periode pengamatan",
        "Missing value"
    ],
    "Jumlah": [
        len(df_co_raw),
        len(df_co),
        df_co["CO"].isna().sum()
    ]
})

ringkasan_missing
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Kondisi</th>
      <th>Jumlah</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Data tersedia dari Sentinel-5P</td>
      <td>197</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Total periode pengamatan</td>
      <td>365</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Missing value</td>
      <td>168</td>
    </tr>
  </tbody>
</table>
</div>



## 6. Data Preprocessing

Tahap preprocessing dilakukan untuk mempersiapkan data CO sebelum digunakan dalam ekstraksi fitur. Tahapan yang dilakukan meliputi penanganan missing value melalui imputation serta identifikasi dan perbaikan outlier.

### 6.1 Missing Value dan Imputation

Missing value pada data CO terjadi karena tidak semua hari dalam periode pengamatan memiliki observasi yang tersedia. Missing value perlu ditangani agar deret waktu memiliki data yang lengkap sebelum dilakukan ekstraksi fitur menggunakan TSFEL.

Pada tahap ini digunakan interpolasi linear untuk memperkirakan nilai CO pada tanggal yang tidak memiliki observasi berdasarkan nilai pada tanggal sebelum dan sesudahnya.


```python
# Membuat salinan data sebelum imputation
df_co_imputed = df_co.copy()

# Imputasi missing value menggunakan interpolasi linear
df_co_imputed["CO"] = (
    df_co_imputed["CO"]
    .interpolate(method="linear")
    .bfill()
    .ffill()
)

# Menyimpan hasil imputation
df_co_imputed.to_csv(
    "ProyekSainsData/data/processed/kualitas_udara_CO_Gubeng_imputed.csv",
    index=False
)
```


```python
ringkasan_imputation = pd.DataFrame({
    "Kondisi": [
        "Sebelum Imputation",
        "Setelah Imputation"
    ],
    "Missing Value": [
        df_co["CO"].isna().sum(),
        df_co_imputed["CO"].isna().sum()
    ]
})

ringkasan_imputation
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Kondisi</th>
      <th>Missing Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sebelum Imputation</td>
      <td>168</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Setelah Imputation</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(14, 5))

plt.plot(
    df_co_imputed["Tanggal"],
    df_co_imputed["CO"]
)

plt.title("Time Series CO Kecamatan Gubeng Setelah Imputation")
plt.xlabel("Tanggal")
plt.ylabel("Konsentrasi CO")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```


    
![png](../img/8_output_27_0.png)



### 6.2 Identifikasi Outlier

Setelah missing value ditangani melalui proses imputation, tahap selanjutnya adalah mengidentifikasi outlier pada data CO. Outlier merupakan nilai yang memiliki perbedaan cukup jauh dibandingkan dengan pola umum data.

Identifikasi outlier dilakukan menggunakan metode Interquartile Range (IQR). Metode ini menggunakan kuartil pertama (Q1) dan kuartil ketiga (Q3) untuk menentukan batas bawah dan batas atas data. Nilai yang berada di luar batas tersebut dikategorikan sebagai outlier.


```python
# Menghitung kuartil dan Interquartile Range (IQR)
Q1 = df_co_imputed["CO"].quantile(0.25)
Q3 = df_co_imputed["CO"].quantile(0.75)
IQR = Q3 - Q1

# Menentukan batas outlier
batas_bawah = Q1 - 1.5 * IQR
batas_atas = Q3 + 1.5 * IQR

# Mengidentifikasi outlier
outlier = (
    (df_co_imputed["CO"] < batas_bawah) |
    (df_co_imputed["CO"] > batas_atas)
)

# Menyimpan data yang teridentifikasi sebagai outlier
df_outlier = df_co_imputed[outlier].copy()
```


```python
ringkasan_outlier = pd.DataFrame({
    "Keterangan": [
        "Q1",
        "Q3",
        "IQR",
        "Batas Bawah",
        "Batas Atas",
        "Jumlah Outlier"
    ],
    "Nilai": [
        Q1,
        Q3,
        IQR,
        batas_bawah,
        batas_atas,
        len(df_outlier)
    ]
})

ringkasan_outlier
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Keterangan</th>
      <th>Nilai</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Q1</td>
      <td>0.026539</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Q3</td>
      <td>0.030859</td>
    </tr>
    <tr>
      <th>2</th>
      <td>IQR</td>
      <td>0.004320</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Batas Bawah</td>
      <td>0.020059</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Batas Atas</td>
      <td>0.037338</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Jumlah Outlier</td>
      <td>9.000000</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(8, 5))

plt.boxplot(
    df_co_imputed["CO"],
    tick_labels=["Sebelum Perbaikan Outlier"]
)

plt.title("Identifikasi Outlier Data CO Kecamatan Gubeng")
plt.ylabel("Konsentrasi CO")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```


    
![png](../img/9_output_31_0.png)



### 6.3 Perbaikan Outlier

Outlier yang telah teridentifikasi perlu diperbaiki agar tidak memberikan pengaruh yang berlebihan terhadap karakteristik deret waktu dan hasil ekstraksi fitur. Pada tahap ini, nilai yang teridentifikasi sebagai outlier diubah menjadi missing value sementara, kemudian diestimasi kembali menggunakan interpolasi linear berdasarkan nilai CO pada waktu sebelum dan sesudahnya.

Pendekatan ini digunakan agar kontinuitas deret waktu tetap dipertahankan tanpa menghilangkan observasi berdasarkan tanggal.


```python
# Menyalin data hasil imputation
df_co_clean = df_co_imputed.copy()

# Menandai nilai outlier sebagai NaN
df_co_clean.loc[outlier, "CO"] = float("nan")

# Memperbaiki outlier menggunakan interpolasi linear
df_co_clean["CO"] = df_co_clean["CO"].interpolate(
    method="linear"
)

# Menangani kemungkinan NaN pada awal atau akhir deret waktu
df_co_clean["CO"] = (
    df_co_clean["CO"]
    .bfill()
    .ffill()
)

# Menyimpan data akhir setelah preprocessing
df_co_clean.to_csv(
    "ProyekSainsData/data/processed/kualitas_udara_CO_Gubeng_clean.csv",
    index=False
)
```


```python
ringkasan_perbaikan = pd.DataFrame({
    "Kondisi": [
        "Sebelum Perbaikan",
        "Setelah Perbaikan"
    ],
    "Jumlah Outlier": [
        len(df_outlier),
        (
            (df_co_clean["CO"] < batas_bawah) |
            (df_co_clean["CO"] > batas_atas)
        ).sum()
    ]
})

ringkasan_perbaikan
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Kondisi</th>
      <th>Jumlah Outlier</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sebelum Perbaikan</td>
      <td>9</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Setelah Perbaikan</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
plt.figure(figsize=(10, 5))

plt.boxplot(
    [
        df_co_imputed["CO"],
        df_co_clean["CO"]
    ],
    tick_labels=[
        "Sebelum Perbaikan",
        "Setelah Perbaikan"
    ]
)

plt.title("Perbandingan Data CO Sebelum dan Setelah Perbaikan Outlier")
plt.ylabel("Konsentrasi CO")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```


    
![png](../img/10_output_35_0.png)




```python
plt.figure(figsize=(14, 5))

plt.plot(
    df_co_clean["Tanggal"],
    df_co_clean["CO"]
)

plt.title("Time Series CO Kecamatan Gubeng Setelah Preprocessing")
plt.xlabel("Tanggal")
plt.ylabel("Konsentrasi CO")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```


    
![png](../img/11_output_36_0.png)



## 7. Ekstraksi Fitur Menggunakan TSFEL

TSFEL (Time Series Feature Extraction Library) digunakan untuk mengekstraksi karakteristik dari deret waktu Karbon Monoksida (CO) yang telah melalui tahap preprocessing. Ekstraksi fitur digunakan untuk mengubah data deret waktu menjadi representasi numerik berdasarkan karakteristik statistik, temporal, spektral, dan fractal.

### 7.1 Persiapan dan Konfigurasi Ekstraksi Fitur

Data CO hasil preprocessing digunakan sebagai sinyal masukan untuk proses ekstraksi fitur. Data memiliki satu observasi per hari sehingga frekuensi sampling ditetapkan sebesar 1 observasi per hari.

Konfigurasi TSFEL kemudian disusun untuk menggunakan 68 jenis fitur yang mencakup fitur statistik, temporal, spektral, dan fractal. Fitur Lempel-Ziv yang secara default tidak aktif diaktifkan agar termasuk dalam daftar fitur yang digunakan. Selain itu, fitur ECDF slope ditambahkan karena fungsi tersebut tersedia dalam TSFEL tetapi tidak terdapat sebagai entri pada konfigurasi fitur default.


```python
# Persiapan data CO untuk ekstraksi fitur

import tsfel
import pandas as pd
import numpy as np

# Mengambil data CO yang telah melalui preprocessing
series_co = df_co_clean["CO"].to_numpy()

# Data memiliki satu observasi setiap hari
fs = 1

print(f"Jumlah data CO: {len(series_co)}")
print(f"Frekuensi sampling: {fs} observasi/hari")

print("\nLima data pertama:")
print(series_co[:5])
```

    Jumlah data CO: 365
    Frekuensi sampling: 1 observasi/hari
    
    Lima data pertama:
    [0.03558657 0.02831089 0.02848885 0.02866681 0.02884477]
    


```python
# Membuat konfigurasi TSFEL menggunakan 68 jenis fitur

cfg_68 = tsfel.get_features_by_domain(
    ["statistical", "temporal", "spectral", "fractal"]
)

# Mengaktifkan Lempel-Ziv complexity
if "Lempel-Ziv complexity" in cfg_68["temporal"]:
    cfg_68["temporal"]["Lempel-Ziv complexity"]["use"] = "yes"

# Menambahkan ECDF slope yang tersedia sebagai fungsi TSFEL
# tetapi tidak terdapat pada features.json default
if hasattr(tsfel, "ecdf_slope"):
    cfg_68["statistical"]["ECDF slope"] = {
        "complexity": "constant",
        "description": "Computes the slope of the ECDF between two percentiles.",
        "function": "tsfel.ecdf_slope",
        "parameters": {
            "p_init": 0.5,
            "p_end": 0.75
        },
        "n_features": 1,
        "use": "yes"
    }
else:
    raise AttributeError(
        "Fungsi ecdf_slope tidak tersedia pada instalasi TSFEL."
    )

# Menghitung jumlah jenis fitur yang aktif
daftar_fitur_68 = []

for domain, fitur_domain in cfg_68.items():
    for nama_fitur, pengaturan in fitur_domain.items():
        if pengaturan["use"] == "yes":
            daftar_fitur_68.append({
                "Domain": domain.capitalize(),
                "Nama Fitur": nama_fitur
            })

df_daftar_fitur_68 = pd.DataFrame(daftar_fitur_68)
df_daftar_fitur_68.insert(
    0,
    "No",
    range(1, len(df_daftar_fitur_68) + 1)
)

jumlah_jenis_fitur = len(df_daftar_fitur_68)

print(f"Jumlah jenis fitur aktif: {jumlah_jenis_fitur}")

display(df_daftar_fitur_68)

if jumlah_jenis_fitur != 68:
    raise ValueError(
        f"Konfigurasi menghasilkan {jumlah_jenis_fitur} jenis fitur, "
        "bukan 68. Periksa konfigurasi TSFEL."
    )
```

    Jumlah jenis fitur aktif: 68
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>Domain</th>
      <th>Nama Fitur</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Statistical</td>
      <td>Absolute energy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Statistical</td>
      <td>Average power</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Statistical</td>
      <td>ECDF</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Statistical</td>
      <td>ECDF Percentile</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Statistical</td>
      <td>ECDF Percentile Count</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>63</th>
      <td>64</td>
      <td>Fractal</td>
      <td>Higuchi fractal dimension</td>
    </tr>
    <tr>
      <th>64</th>
      <td>65</td>
      <td>Fractal</td>
      <td>Hurst exponent</td>
    </tr>
    <tr>
      <th>65</th>
      <td>66</td>
      <td>Fractal</td>
      <td>Maximum fractal length</td>
    </tr>
    <tr>
      <th>66</th>
      <td>67</td>
      <td>Fractal</td>
      <td>Petrosian fractal dimension</td>
    </tr>
    <tr>
      <th>67</th>
      <td>68</td>
      <td>Fractal</td>
      <td>Multiscale entropy</td>
    </tr>
  </tbody>
</table>
<p>68 rows × 3 columns</p>
</div>


### 7.2 Ekstraksi dan Penyimpanan Hasil

Setelah konfigurasi 68 jenis fitur terbentuk, proses ekstraksi dilakukan terhadap deret waktu CO yang telah melalui preprocessing. TSFEL menghasilkan representasi numerik dari karakteristik deret waktu berdasarkan konfigurasi yang telah ditentukan.

Hasil ekstraksi kemudian disimpan dalam format CSV agar dapat digunakan pada tahap analisis fitur selanjutnya.


```python
# Ekstraksi 68 jenis fitur TSFEL pada data CO
# Menggunakan fungsi internal TSFEL untuk menghindari masalah
# duplicate column pada proses reindex bawaan.

from tsfel.feature_extraction.calc_features import calc_window_features

features_68_co = calc_window_features(
    cfg_68,
    series_co,
    fs,
    single_window=True
)

# Memastikan hasil berbentuk DataFrame
if not isinstance(features_68_co, pd.DataFrame):
    features_68_co = pd.DataFrame(features_68_co)

print(f"Jumlah baris hasil ekstraksi: {features_68_co.shape[0]}")
print(f"Jumlah kolom output fitur: {features_68_co.shape[1]}")

display(features_68_co)
```



<p>
    Progress: 100% Complete
<p/>
<progress
    value='68'
    max='68',
    style='width: 25%',
>
    68
</progress>




    Jumlah baris hasil ekstraksi: 1
    Jumlah kolom output fitur: 164
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0_Absolute energy</th>
      <th>0_Average power</th>
      <th>0_ECDF_0</th>
      <th>0_ECDF_1</th>
      <th>0_ECDF_2</th>
      <th>0_ECDF_3</th>
      <th>0_ECDF_4</th>
      <th>0_ECDF_5</th>
      <th>0_ECDF_6</th>
      <th>0_ECDF_7</th>
      <th>...</th>
      <th>0_Wavelet variance_0.04Hz</th>
      <th>0_Wavelet variance_0.04Hz</th>
      <th>0_Wavelet variance_0.03Hz</th>
      <th>0_Wavelet variance_0.03Hz</th>
      <th>0_Detrended fluctuation analysis</th>
      <th>0_Higuchi fractal dimension</th>
      <th>0_Hurst exponent</th>
      <th>0_Maximum fractal length</th>
      <th>0_Petrosian fractal dimension</th>
      <th>0_Multiscale entropy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.302971</td>
      <td>0.000832</td>
      <td>0.00274</td>
      <td>0.005479</td>
      <td>0.008219</td>
      <td>0.010959</td>
      <td>0.013699</td>
      <td>0.016438</td>
      <td>0.019178</td>
      <td>0.021918</td>
      <td>...</td>
      <td>0.000073</td>
      <td>0.00009</td>
      <td>0.000109</td>
      <td>0.000131</td>
      <td>0.853424</td>
      <td>1.909033</td>
      <td>0.754635</td>
      <td>0.037436</td>
      <td>1.023776</td>
      <td>1.209065</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 164 columns</p>
</div>



```python
# Pemeriksaan dan perapihan nama kolom hasil ekstraksi

print("=== Pemeriksaan Hasil Ekstraksi TSFEL ===")
print(f"Jumlah jenis fitur yang dikonfigurasi : {jumlah_jenis_fitur}")
print(f"Jumlah output numerik yang dihasilkan : {features_68_co.shape[1]}")

# Mengidentifikasi nama kolom yang duplikat
kolom_duplikat = features_68_co.columns[
    features_68_co.columns.duplicated(keep=False)
]

print(f"Jumlah nama kolom duplikat            : {len(kolom_duplikat.unique())}")

if len(kolom_duplikat) > 0:
    print("\nNama kolom yang duplikat:")
    for nama in kolom_duplikat.unique():
        print(f"- {nama}")

    # Membuat seluruh nama kolom menjadi unik
    nama_baru = []
    penghitung = {}

    for nama in features_68_co.columns:
        if nama not in penghitung:
            penghitung[nama] = 1
            nama_baru.append(nama)
        else:
            penghitung[nama] += 1
            nama_baru.append(
                f"{nama}_{penghitung[nama]}"
            )

    features_68_co.columns = nama_baru

    print("\nNama kolom telah dibuat unik.")
else:
    print("\nTidak terdapat nama kolom duplikat.")

# Pemeriksaan akhir
jumlah_kolom_duplikat_akhir = (
    features_68_co.columns.duplicated().sum()
)

print(f"\nJumlah nama kolom duplikat setelah perapihan: "
      f"{jumlah_kolom_duplikat_akhir}")

if jumlah_jenis_fitur == 68:
    print("✓ Konfigurasi berhasil menggunakan 68 jenis fitur.")

if jumlah_kolom_duplikat_akhir == 0:
    print("✓ Seluruh nama output fitur sekarang unik.")
```

    === Pemeriksaan Hasil Ekstraksi TSFEL ===
    Jumlah jenis fitur yang dikonfigurasi : 68
    Jumlah output numerik yang dihasilkan : 164
    Jumlah nama kolom duplikat            : 8
    
    Nama kolom yang duplikat:
    - 0_Wavelet absolute mean_0.04Hz
    - 0_Wavelet absolute mean_0.03Hz
    - 0_Wavelet energy_0.04Hz
    - 0_Wavelet energy_0.03Hz
    - 0_Wavelet standard deviation_0.04Hz
    - 0_Wavelet standard deviation_0.03Hz
    - 0_Wavelet variance_0.04Hz
    - 0_Wavelet variance_0.03Hz
    
    Nama kolom telah dibuat unik.
    
    Jumlah nama kolom duplikat setelah perapihan: 0
    ✓ Konfigurasi berhasil menggunakan 68 jenis fitur.
    ✓ Seluruh nama output fitur sekarang unik.
    


```python
# Menyimpan hasil ekstraksi 68 jenis fitur TSFEL

output_fitur_68 = (
    "ProyekSainsData/data/processed/"
    "fitur_TSFEL_CO_Gubeng_68_fitur.csv"
)

features_68_co.to_csv(
    output_fitur_68,
    index=False
)

print("Hasil ekstraksi 68 jenis fitur TSFEL berhasil disimpan.")
print(f"Jumlah jenis fitur : {jumlah_jenis_fitur}")
print(f"Jumlah output fitur : {features_68_co.shape[1]}")
print(f"Lokasi file        : {output_fitur_68}")
```

    Hasil ekstraksi 68 jenis fitur TSFEL berhasil disimpan.
    Jumlah jenis fitur : 68
    Jumlah output fitur : 164
    Lokasi file        : ProyekSainsData/data/processed/fitur_TSFEL_CO_Gubeng_68_fitur.csv
    

## 8. Analisis Fitur TSFEL

Hasil ekstraksi TSFEL selanjutnya dianalisis untuk mengetahui karakteristik deret waktu Karbon Monoksida (CO) pada Kecamatan Gubeng. Analisis menggunakan konfigurasi yang terdiri dari 68 jenis fitur dari berbagai karakteristik deret waktu.

Perlu dibedakan antara jumlah jenis fitur dan jumlah output numerik. Sebanyak 68 jenis fitur digunakan dalam konfigurasi, sedangkan hasil ekstraksi menghasilkan 164 output numerik. Perbedaan jumlah tersebut terjadi karena beberapa jenis fitur menghasilkan lebih dari satu nilai keluaran.

Analisis dilakukan dengan melihat daftar fitur yang digunakan, jumlah output yang dihasilkan, serta nilai masing-masing output fitur pada deret waktu CO setelah preprocessing.


```python
# Ringkasan hasil ekstraksi TSFEL

print("=== Ringkasan Hasil Ekstraksi TSFEL ===")
print(f"Jumlah jenis fitur yang digunakan : {jumlah_jenis_fitur}")
print(f"Jumlah output numerik            : {features_68_co.shape[1]}")
print(f"Jumlah data hasil ekstraksi      : {features_68_co.shape[0]}")

print("\nJumlah jenis fitur berdasarkan domain:")

ringkasan_domain = (
    df_daftar_fitur_68
    .groupby("Domain")
    .size()
    .reset_index(name="Jumlah Jenis Fitur")
)

display(ringkasan_domain)
```

    === Ringkasan Hasil Ekstraksi TSFEL ===
    Jumlah jenis fitur yang digunakan : 68
    Jumlah output numerik            : 164
    Jumlah data hasil ekstraksi      : 1
    
    Jumlah jenis fitur berdasarkan domain:
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Domain</th>
      <th>Jumlah Jenis Fitur</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Fractal</td>
      <td>6</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Spectral</td>
      <td>26</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Statistical</td>
      <td>21</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Temporal</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
</div>



```python
# Menampilkan daftar 68 jenis fitur yang digunakan

print("=== Daftar 68 Jenis Fitur TSFEL ===")

display(
    df_daftar_fitur_68[
        ["No", "Domain", "Nama Fitur"]
    ]
)
```

    === Daftar 68 Jenis Fitur TSFEL ===
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>Domain</th>
      <th>Nama Fitur</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Statistical</td>
      <td>Absolute energy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Statistical</td>
      <td>Average power</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Statistical</td>
      <td>ECDF</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Statistical</td>
      <td>ECDF Percentile</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Statistical</td>
      <td>ECDF Percentile Count</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>63</th>
      <td>64</td>
      <td>Fractal</td>
      <td>Higuchi fractal dimension</td>
    </tr>
    <tr>
      <th>64</th>
      <td>65</td>
      <td>Fractal</td>
      <td>Hurst exponent</td>
    </tr>
    <tr>
      <th>65</th>
      <td>66</td>
      <td>Fractal</td>
      <td>Maximum fractal length</td>
    </tr>
    <tr>
      <th>66</th>
      <td>67</td>
      <td>Fractal</td>
      <td>Petrosian fractal dimension</td>
    </tr>
    <tr>
      <th>67</th>
      <td>68</td>
      <td>Fractal</td>
      <td>Multiscale entropy</td>
    </tr>
  </tbody>
</table>
<p>68 rows × 3 columns</p>
</div>



```python
# Menampilkan seluruh output numerik hasil ekstraksi

hasil_fitur_68 = pd.DataFrame({
    "Nama Output Fitur": features_68_co.columns,
    "Nilai": features_68_co.iloc[0].values
})

hasil_fitur_68.insert(
    0,
    "No",
    range(1, len(hasil_fitur_68) + 1)
)

print("=== Nilai 164 Output Numerik TSFEL ===")

display(hasil_fitur_68)
```

    === Nilai 164 Output Numerik TSFEL ===
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>Nama Output Fitur</th>
      <th>Nilai</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0_Absolute energy</td>
      <td>0.302971</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>0_Average power</td>
      <td>0.000832</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>0_ECDF_0</td>
      <td>0.002740</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>0_ECDF_1</td>
      <td>0.005479</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0_ECDF_2</td>
      <td>0.008219</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>159</th>
      <td>160</td>
      <td>0_Higuchi fractal dimension</td>
      <td>1.909033</td>
    </tr>
    <tr>
      <th>160</th>
      <td>161</td>
      <td>0_Hurst exponent</td>
      <td>0.754635</td>
    </tr>
    <tr>
      <th>161</th>
      <td>162</td>
      <td>0_Maximum fractal length</td>
      <td>0.037436</td>
    </tr>
    <tr>
      <th>162</th>
      <td>163</td>
      <td>0_Petrosian fractal dimension</td>
      <td>1.023776</td>
    </tr>
    <tr>
      <th>163</th>
      <td>164</td>
      <td>0_Multiscale entropy</td>
      <td>1.209065</td>
    </tr>
  </tbody>
</table>
<p>164 rows × 3 columns</p>
</div>



```python
# Ringkasan nilai output fitur

ringkasan_output = hasil_fitur_68["Nilai"].describe()

print("=== Ringkasan Nilai Output Fitur ===")

display(
    ringkasan_output.to_frame(
        name="Nilai"
    )
)
```

    === Ringkasan Nilai Output Fitur ===
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Nilai</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>164.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>2.505799</td>
    </tr>
    <tr>
      <th>std</th>
      <td>101.826718</td>
    </tr>
    <tr>
      <th>min</th>
      <td>-1168.806518</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>0.000022</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>0.004695</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>0.449580</td>
    </tr>
    <tr>
      <th>max</th>
      <td>364.002006</td>
    </tr>
  </tbody>
</table>
</div>


Hasil ekstraksi menunjukkan bahwa sebanyak 68 jenis fitur TSFEL berhasil digunakan pada data deret waktu Karbon Monoksida (CO) Kecamatan Gubeng. Fitur tersebut terdiri dari 21 fitur statistik, 15 fitur temporal, 26 fitur spektral, dan 6 fitur fractal.

Dari 68 jenis fitur tersebut diperoleh 164 output numerik. Jumlah output lebih besar daripada jumlah jenis fitur karena beberapa fitur menghasilkan lebih dari satu nilai keluaran. Hasil tersebut digunakan sebagai representasi numerik dari karakteristik deret waktu CO setelah melalui tahap preprocessing.

Fitur statistik menggambarkan karakteristik nilai dan distribusi sinyal, fitur temporal menggambarkan perubahan sinyal terhadap waktu, fitur spektral menggambarkan karakteristik berdasarkan komponen frekuensi, sedangkan fitur fractal menggambarkan karakteristik kompleksitas dan struktur deret waktu.

## 9. Analisis Kemiripan CO dan CO₂

Analisis kemiripan dilakukan untuk membandingkan karakteristik deret waktu Karbon Monoksida (CO) dan Karbon Dioksida (CO₂). Data CO diperoleh dari Sentinel-5P pada Kecamatan Gubeng, sedangkan data CO₂ diperoleh dari hasil pengukuran kualitas udara di Kampus ITS Surabaya.

Karena kedua dataset memiliki periode pengamatan yang berbeda, analisis dilakukan hanya pada tanggal yang tersedia pada kedua dataset. Data CO₂ yang memiliki resolusi pengamatan per menit telah diagregasi menjadi nilai rata-rata harian sehingga memiliki resolusi waktu yang sama dengan data CO.

Setelah kedua dataset diselaraskan berdasarkan tanggal, data yang memiliki nilai lengkap pada kedua parameter digunakan untuk analisis. Selanjutnya, 68 jenis fitur TSFEL diterapkan secara konsisten pada deret waktu CO dan CO₂ untuk memperoleh representasi karakteristik masing-masing deret waktu.

Kemiripan dianalisis melalui visualisasi deret waktu serta perbandingan representasi output fitur TSFEL menggunakan Cosine Similarity dan korelasi Pearson. Hasil analisis digunakan untuk melihat apakah karakteristik deret waktu CO dan CO₂ menunjukkan kemiripan berdasarkan representasi fitur TSFEL pada periode pengamatan yang sama.

### 9.1 Penyelarasan Data CO dan CO₂

Data CO dan CO₂ terlebih dahulu diselaraskan berdasarkan tanggal pengamatan. Karena kedua dataset memiliki periode pengamatan yang berbeda, analisis hanya dilakukan pada tanggal yang tersedia pada kedua dataset.

Data CO₂ yang memiliki resolusi pengamatan per menit telah diagregasi menjadi nilai rata-rata harian sehingga memiliki resolusi waktu yang sama dengan data CO. Setelah kedua dataset digabungkan berdasarkan tanggal, baris yang tidak memiliki nilai lengkap pada kedua parameter dihapus.

Hasil penyelarasan menghasilkan 102 hari pengamatan yang dapat digunakan untuk analisis kemiripan.


```python
# Menyelaraskan data CO dan CO₂ berdasarkan tanggal

tanggal_mulai_kemiripan = max(
    df_co_clean["Tanggal"].min(),
    df_co2_harian["Tanggal"].min()
)

tanggal_akhir_kemiripan = min(
    df_co_clean["Tanggal"].max(),
    df_co2_harian["Tanggal"].max()
)

# Mengambil data pada periode yang sama
df_co_kemiripan = df_co_clean[
    (df_co_clean["Tanggal"] >= tanggal_mulai_kemiripan) &
    (df_co_clean["Tanggal"] <= tanggal_akhir_kemiripan)
][["Tanggal", "CO"]].copy()

df_co2_kemiripan = df_co2_harian[
    (df_co2_harian["Tanggal"] >= tanggal_mulai_kemiripan) &
    (df_co2_harian["Tanggal"] <= tanggal_akhir_kemiripan)
][["Tanggal", "CO2"]].copy()

# Menggabungkan berdasarkan tanggal
df_kemiripan = pd.merge(
    df_co_kemiripan,
    df_co2_kemiripan,
    on="Tanggal",
    how="inner"
)

# Menghapus baris yang masih memiliki missing value
df_kemiripan = (
    df_kemiripan
    .dropna(subset=["CO", "CO2"])
    .sort_values("Tanggal")
    .reset_index(drop=True)
)

print("=== Periode Analisis Kemiripan ===")
print(
    f"Periode: {df_kemiripan['Tanggal'].min().date()} "
    f"sampai {df_kemiripan['Tanggal'].max().date()}"
)
print(f"Jumlah hari yang dapat dibandingkan: {len(df_kemiripan)} hari")

display(df_kemiripan.head(10))
```

    === Periode Analisis Kemiripan ===
    Periode: 2025-08-24 sampai 2025-12-11
    Jumlah hari yang dapat dibandingkan: 102 hari
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Tanggal</th>
      <th>CO</th>
      <th>CO2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2025-08-24</td>
      <td>0.035587</td>
      <td>413.960000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2025-08-25</td>
      <td>0.028311</td>
      <td>426.921569</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2025-08-26</td>
      <td>0.028489</td>
      <td>425.769231</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2025-08-27</td>
      <td>0.028667</td>
      <td>420.801980</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2025-08-28</td>
      <td>0.028845</td>
      <td>421.135417</td>
    </tr>
    <tr>
      <th>5</th>
      <td>2025-08-29</td>
      <td>0.022107</td>
      <td>423.333333</td>
    </tr>
    <tr>
      <th>6</th>
      <td>2025-08-30</td>
      <td>0.026482</td>
      <td>419.062500</td>
    </tr>
    <tr>
      <th>7</th>
      <td>2025-08-31</td>
      <td>0.024324</td>
      <td>416.750000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>2025-09-01</td>
      <td>0.022166</td>
      <td>464.217391</td>
    </tr>
    <tr>
      <th>9</th>
      <td>2025-09-02</td>
      <td>0.022403</td>
      <td>414.345652</td>
    </tr>
  </tbody>
</table>
</div>



```python
# Visualisasi perbandingan deret waktu CO dan CO₂

fig, ax1 = plt.subplots(figsize=(14, 5))

ax1.plot(
    df_kemiripan["Tanggal"],
    df_kemiripan["CO"],
    label="CO"
)

ax1.set_xlabel("Tanggal")
ax1.set_ylabel("CO")
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()

ax2.plot(
    df_kemiripan["Tanggal"],
    df_kemiripan["CO2"],
    linestyle="--",
    label="CO₂"
)

ax2.set_ylabel("CO₂ (ppm)")

plt.title(
    "Perbandingan Deret Waktu CO dan CO₂ "
    "pada Periode Pengamatan yang Sama"
)

fig.tight_layout()
plt.show()
```


    
![png](../img/12_output_54_0.png)
    



```python
# Menyiapkan deret waktu CO dan CO₂ untuk ekstraksi fitur

series_co_compare = df_kemiripan["CO"].to_numpy(dtype=float)
series_co2_compare = df_kemiripan["CO2"].to_numpy(dtype=float)

fs_compare = 1

print("=== Persiapan Ekstraksi Fitur untuk Analisis Kemiripan ===")
print(f"Jumlah data CO  : {len(series_co_compare)}")
print(f"Jumlah data CO₂ : {len(series_co2_compare)}")
print(f"Frekuensi sampling: {fs_compare} observasi/hari")

if len(series_co_compare) != len(series_co2_compare):
    raise ValueError(
        "Jumlah titik data CO dan CO₂ tidak sama."
    )
```

    === Persiapan Ekstraksi Fitur untuk Analisis Kemiripan ===
    Jumlah data CO  : 102
    Jumlah data CO₂ : 102
    Frekuensi sampling: 1 observasi/hari
    

### 9.2 Ekstraksi 68 Fitur TSFEL

Pada tahap ini, 68 jenis fitur TSFEL diterapkan pada deret waktu CO dan CO₂ yang telah diselaraskan berdasarkan tanggal.

Agar perbandingan fitur dilakukan secara konsisten, data CO dan CO₂ yang digunakan memiliki periode dan jumlah titik pengamatan yang sama, yaitu 102 hari pengamatan yang tersedia pada kedua dataset.

Ekstraksi dilakukan menggunakan satu window yang mencakup seluruh periode pengamatan. Karena beberapa jenis fitur TSFEL dapat menghasilkan lebih dari satu nilai output, jumlah output numerik yang dihasilkan dapat lebih besar daripada jumlah jenis fitur yang digunakan.



```python
# Ekstraksi 68 jenis fitur TSFEL pada data CO₂

import warnings

with warnings.catch_warnings(record=True) as warning_tsfel:
    warnings.simplefilter("always")

    features_68_co2 = calc_window_features(
        cfg_68,
        series_co2_compare,
        fs_compare,
        single_window=True
    )

# Memastikan hasil berbentuk DataFrame
if not isinstance(features_68_co2, pd.DataFrame):
    features_68_co2 = pd.DataFrame(features_68_co2)

print("=== Hasil Ekstraksi Fitur CO₂ ===")
print(f"Jumlah jenis fitur : {jumlah_jenis_fitur}")
print(f"Jumlah output fitur: {features_68_co2.shape[1]}")
print(f"Jumlah baris       : {features_68_co2.shape[0]}")

# Menjelaskan keterbatasan fitur fractal
if warning_tsfel:
    print("\nCatatan:")
    print(
        "Beberapa fitur fractal tidak dapat dihitung karena "
        "jumlah data CO₂ yang tersedia kurang dari 160 titik."
    )
    
    print(
        "Output fitur yang tidak dapat dihitung akan menghasilkan "
        "nilai NaN dan tidak digunakan dalam analisis kemiripan."
    )

display(features_68_co2)
```



<p>
    Progress: 100% Complete
<p/>
<progress
    value='68'
    max='68',
    style='width: 25%',
>
    68
</progress>




    === Hasil Ekstraksi Fitur CO₂ ===
    Jumlah jenis fitur : 68
    Jumlah output fitur: 164
    Jumlah baris       : 1
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0_Absolute energy</th>
      <th>0_Average power</th>
      <th>0_ECDF_0</th>
      <th>0_ECDF_1</th>
      <th>0_ECDF_2</th>
      <th>0_ECDF_3</th>
      <th>0_ECDF_4</th>
      <th>0_ECDF_5</th>
      <th>0_ECDF_6</th>
      <th>0_ECDF_7</th>
      <th>...</th>
      <th>0_Wavelet variance_0.04Hz</th>
      <th>0_Wavelet variance_0.04Hz</th>
      <th>0_Wavelet variance_0.03Hz</th>
      <th>0_Wavelet variance_0.03Hz</th>
      <th>0_Detrended fluctuation analysis</th>
      <th>0_Higuchi fractal dimension</th>
      <th>0_Hurst exponent</th>
      <th>0_Maximum fractal length</th>
      <th>0_Petrosian fractal dimension</th>
      <th>0_Multiscale entropy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.839738e+07</td>
      <td>182152.266767</td>
      <td>0.009804</td>
      <td>0.019608</td>
      <td>0.029412</td>
      <td>0.039216</td>
      <td>0.04902</td>
      <td>0.058824</td>
      <td>0.068627</td>
      <td>0.078431</td>
      <td>...</td>
      <td>32192.222416</td>
      <td>41419.500984</td>
      <td>50569.653766</td>
      <td>59283.22873</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.050881</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 164 columns</p>
</div>



```python
# Ekstraksi 68 jenis fitur TSFEL pada data CO
# menggunakan periode pengamatan yang sama dengan CO₂

features_68_co_compare = calc_window_features(
    cfg_68,
    series_co_compare,
    fs_compare,
    single_window=True
)

# Memastikan hasil berbentuk DataFrame
if not isinstance(features_68_co_compare, pd.DataFrame):
    features_68_co_compare = pd.DataFrame(features_68_co_compare)

print("=== Hasil Ekstraksi Fitur CO ===")
print(f"Jumlah jenis fitur : {jumlah_jenis_fitur}")
print(f"Jumlah output fitur: {features_68_co_compare.shape[1]}")
print(f"Jumlah baris       : {features_68_co_compare.shape[0]}")

display(features_68_co_compare)
```



<p>
    Progress: 100% Complete
<p/>
<progress
    value='68'
    max='68',
    style='width: 25%',
>
    68
</progress>




    === Hasil Ekstraksi Fitur CO ===
    Jumlah jenis fitur : 68
    Jumlah output fitur: 164
    Jumlah baris       : 1
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0_Absolute energy</th>
      <th>0_Average power</th>
      <th>0_ECDF_0</th>
      <th>0_ECDF_1</th>
      <th>0_ECDF_2</th>
      <th>0_ECDF_3</th>
      <th>0_ECDF_4</th>
      <th>0_ECDF_5</th>
      <th>0_ECDF_6</th>
      <th>0_ECDF_7</th>
      <th>...</th>
      <th>0_Wavelet variance_0.04Hz</th>
      <th>0_Wavelet variance_0.04Hz</th>
      <th>0_Wavelet variance_0.03Hz</th>
      <th>0_Wavelet variance_0.03Hz</th>
      <th>0_Detrended fluctuation analysis</th>
      <th>0_Higuchi fractal dimension</th>
      <th>0_Hurst exponent</th>
      <th>0_Maximum fractal length</th>
      <th>0_Petrosian fractal dimension</th>
      <th>0_Multiscale entropy</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.088638</td>
      <td>0.000878</td>
      <td>0.009804</td>
      <td>0.019608</td>
      <td>0.029412</td>
      <td>0.039216</td>
      <td>0.04902</td>
      <td>0.058824</td>
      <td>0.068627</td>
      <td>0.078431</td>
      <td>...</td>
      <td>0.00016</td>
      <td>0.000194</td>
      <td>0.000232</td>
      <td>0.000262</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.026231</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 164 columns</p>
</div>


### 9.3 Pemeriksaan Output Fitur

Hasil ekstraksi fitur diperiksa untuk mengetahui apakah terdapat output fitur yang menghasilkan nilai NaN pada data CO dan CO₂. Kondisi tersebut dapat terjadi pada beberapa fitur yang memiliki persyaratan jumlah titik data minimum tertentu.

Output fitur yang tidak dapat dihitung pada salah satu parameter tidak digunakan dalam perbandingan. Dengan demikian, analisis kemiripan hanya menggunakan output fitur yang memiliki nilai lengkap pada kedua parameter.


```python
# Pemeriksaan output fitur CO₂ yang tidak dapat dihitung

jumlah_nan_co2 = features_68_co2.isna().sum().sum()
kolom_nan_co2 = features_68_co2.columns[
    features_68_co2.isna().any()
]

print("=== Pemeriksaan Missing Value Hasil TSFEL CO₂ ===")
print(f"Jumlah seluruh output fitur : {features_68_co2.shape[1]}")
print(f"Jumlah nilai NaN             : {jumlah_nan_co2}")
print(f"Jumlah output yang memiliki NaN: {len(kolom_nan_co2)}")

print("\nOutput fitur yang memiliki NaN:")

for nama in kolom_nan_co2:
    print(f"- {nama}")
```

    === Pemeriksaan Missing Value Hasil TSFEL CO₂ ===
    Jumlah seluruh output fitur : 164
    Jumlah nilai NaN             : 5
    Jumlah output yang memiliki NaN: 5
    
    Output fitur yang memiliki NaN:
    - 0_Detrended fluctuation analysis
    - 0_Higuchi fractal dimension
    - 0_Hurst exponent
    - 0_Maximum fractal length
    - 0_Multiscale entropy
    


```python
# Menyiapkan output fitur yang valid untuk perbandingan CO dan CO₂

jumlah_output_co = features_68_co_compare.shape[1]
jumlah_output_co2 = features_68_co2.shape[1]

print("=== Pemeriksaan Output Fitur ===")
print(f"Jumlah output fitur CO  : {jumlah_output_co}")
print(f"Jumlah output fitur CO₂ : {jumlah_output_co2}")

if jumlah_output_co != jumlah_output_co2:
    raise ValueError(
        "Jumlah output fitur CO dan CO₂ tidak sama."
    )

# Memeriksa output fitur yang memiliki nilai lengkap
valid_co = ~features_68_co_compare.isna().all(axis=0).to_numpy()
valid_co2 = ~features_68_co2.isna().all(axis=0).to_numpy()

# Hanya menggunakan output yang valid pada kedua data
mask_valid = valid_co & valid_co2

kolom_valid = features_68_co_compare.columns[mask_valid]

fitur_co_valid = features_68_co_compare.loc[:, mask_valid].copy()
fitur_co2_valid = features_68_co2.loc[:, mask_valid].copy()

print("\n=== Output Fitur yang Digunakan untuk Perbandingan ===")
print(f"Total output fitur hasil ekstraksi : {jumlah_output_co}")
print(f"Output fitur valid pada kedua data : {len(kolom_valid)}")
print(
    f"Output fitur tidak digunakan       : "
    f"{jumlah_output_co - len(kolom_valid)}"
)

print("\nOutput fitur yang tidak digunakan:")

kolom_tidak_valid = features_68_co_compare.columns[~mask_valid]

for nama in kolom_tidak_valid:
    print(f"- {nama}")

print("\nLima output pertama yang digunakan:")

display(
    pd.DataFrame({
        "No": range(1, min(6, len(kolom_valid) + 1)),
        "Nama Output Fitur": kolom_valid[:5]
    })
)
```

    === Pemeriksaan Output Fitur ===
    Jumlah output fitur CO  : 164
    Jumlah output fitur CO₂ : 164
    
    === Output Fitur yang Digunakan untuk Perbandingan ===
    Total output fitur hasil ekstraksi : 164
    Output fitur valid pada kedua data : 159
    Output fitur tidak digunakan       : 5
    
    Output fitur yang tidak digunakan:
    - 0_Detrended fluctuation analysis
    - 0_Higuchi fractal dimension
    - 0_Hurst exponent
    - 0_Maximum fractal length
    - 0_Multiscale entropy
    
    Lima output pertama yang digunakan:
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>No</th>
      <th>Nama Output Fitur</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0_Absolute energy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>0_Average power</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>0_ECDF_0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>0_ECDF_1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0_ECDF_2</td>
    </tr>
  </tbody>
</table>
</div>


### 9.4 Perbandingan Output Fitur CO dan CO₂

Output fitur dari deret waktu CO dan CO₂ dibandingkan berdasarkan posisi kolom yang sama. Hanya output fitur yang memiliki nilai lengkap pada kedua parameter yang digunakan dalam analisis kemiripan.

Berdasarkan hasil pemeriksaan, terdapat 164 output fitur hasil ekstraksi. Sebanyak 159 output fitur memiliki nilai lengkap pada kedua parameter, sedangkan 5 output fitur tidak digunakan karena menghasilkan nilai NaN pada data CO₂.


```python
# Membandingkan nilai output fitur CO dan CO₂

tabel_perbandingan = pd.DataFrame({
    "Nama Output Fitur": kolom_valid,
    "CO": fitur_co_valid.iloc[0].to_numpy(),
    "CO₂": fitur_co2_valid.iloc[0].to_numpy()
})

print("=== Tabel Perbandingan Output Fitur CO dan CO₂ ===")
print(f"Jumlah output fitur yang dibandingkan: {len(tabel_perbandingan)}")

display(tabel_perbandingan)
```

    === Tabel Perbandingan Output Fitur CO dan CO₂ ===
    Jumlah output fitur yang dibandingkan: 159
    


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Nama Output Fitur</th>
      <th>CO</th>
      <th>CO₂</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0_Absolute energy</td>
      <td>0.302971</td>
      <td>1.839738e+07</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0_Average power</td>
      <td>0.000832</td>
      <td>1.821523e+05</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0_ECDF_0</td>
      <td>0.002740</td>
      <td>9.803922e-03</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0_ECDF_1</td>
      <td>0.005479</td>
      <td>1.960784e-02</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0_ECDF_2</td>
      <td>0.008219</td>
      <td>2.941176e-02</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>154</th>
      <td>0_Wavelet variance_0.04Hz</td>
      <td>0.000073</td>
      <td>3.219222e+04</td>
    </tr>
    <tr>
      <th>155</th>
      <td>0_Wavelet variance_0.04Hz_2</td>
      <td>0.000090</td>
      <td>4.141950e+04</td>
    </tr>
    <tr>
      <th>156</th>
      <td>0_Wavelet variance_0.03Hz</td>
      <td>0.000109</td>
      <td>5.056965e+04</td>
    </tr>
    <tr>
      <th>157</th>
      <td>0_Wavelet variance_0.03Hz_2</td>
      <td>0.000131</td>
      <td>5.928323e+04</td>
    </tr>
    <tr>
      <th>158</th>
      <td>0_Petrosian fractal dimension</td>
      <td>1.023776</td>
      <td>1.050881e+00</td>
    </tr>
  </tbody>
</table>
<p>159 rows × 3 columns</p>
</div>


### 9.5 Cosine Similarity

Cosine Similarity digunakan untuk mengukur tingkat kemiripan arah antara vektor output fitur CO dan CO₂. Perhitungan dilakukan menggunakan output fitur yang memiliki nilai lengkap pada kedua parameter.


```python
# Menghitung Cosine Similarity antara fitur CO dan CO₂

from sklearn.metrics.pairwise import cosine_similarity

# Mengambil vektor fitur CO dan CO₂
vektor_co = fitur_co_valid.iloc[0].to_numpy(dtype=float)
vektor_co2 = fitur_co2_valid.iloc[0].to_numpy(dtype=float)

# Menghitung cosine similarity
nilai_cosine = cosine_similarity(
    vektor_co.reshape(1, -1),
    vektor_co2.reshape(1, -1)
)[0, 0]

print("=== Cosine Similarity CO dan CO₂ ===")
print(f"Jumlah output fitur yang digunakan : {len(kolom_valid)}")
print(f"Nilai Cosine Similarity            : {nilai_cosine:.6f}")
```

    === Cosine Similarity CO dan CO₂ ===
    Jumlah output fitur yang digunakan : 159
    Nilai Cosine Similarity            : 0.018474
    

**Interpretasi**

Nilai Cosine Similarity yang diperoleh adalah 0.018474. Nilai tersebut sangat dekat dengan 0 sehingga menunjukkan bahwa arah vektor karakteristik yang direpresentasikan oleh output fitur CO dan CO₂ memiliki tingkat kemiripan yang sangat rendah.

Hasil ini menunjukkan bahwa berdasarkan representasi fitur TSFEL, karakteristik CO dan CO₂ pada periode pengamatan yang sama tidak memiliki kemiripan arah vektor yang kuat.

### 9.6 Korelasi Pearson

Selain Cosine Similarity, korelasi Pearson digunakan untuk mengukur hubungan linear antara output fitur CO dan CO₂. Nilai korelasi Pearson berada pada rentang -1 sampai 1, dengan nilai positif menunjukkan hubungan searah dan nilai negatif menunjukkan hubungan berlawanan arah.

Perhitungan dilakukan menggunakan 159 output fitur yang memiliki nilai lengkap pada kedua parameter.


```python
# Menghitung korelasi Pearson antara output fitur CO dan CO₂

from scipy.stats import pearsonr

# Mengambil nilai fitur yang valid pada kedua data
x = fitur_co_valid.iloc[0].to_numpy(dtype=float)
y = fitur_co2_valid.iloc[0].to_numpy(dtype=float)

# Menghitung korelasi Pearson
nilai_korelasi, nilai_p = pearsonr(x, y)

print("=== Korelasi Pearson Fitur CO dan CO₂ ===")
print(f"Jumlah output fitur yang digunakan : {len(kolom_valid)}")
print(f"Nilai Korelasi Pearson             : {nilai_korelasi:.6f}")
print(f"Nilai p-value                      : {nilai_p:.6f}")
```

    === Korelasi Pearson Fitur CO dan CO₂ ===
    Jumlah output fitur yang digunakan : 159
    Nilai Korelasi Pearson             : 0.008837
    Nilai p-value                      : 0.911976
    

**Interpretasi**

Nilai korelasi Pearson yang diperoleh adalah 0.008837. Nilai tersebut sangat dekat dengan 0 sehingga menunjukkan bahwa hubungan linear antara output fitur CO dan CO₂ sangat lemah.

Nilai p-value yang diperoleh adalah 0.911976. Karena nilai p-value lebih besar dari 0.05, tidak terdapat bukti yang cukup untuk menyatakan adanya hubungan linear yang signifikan antara output fitur CO dan CO₂ pada tingkat signifikansi 5%.

Dengan demikian, berdasarkan 159 output fitur TSFEL yang memiliki nilai lengkap pada kedua parameter, CO dan CO₂ tidak menunjukkan hubungan linear yang signifikan pada periode pengamatan yang sama.

### 9.7 Kesimpulan Analisis Kemiripan

Berdasarkan hasil analisis menggunakan 159 output fitur TSFEL yang memiliki nilai lengkap pada kedua parameter, diperoleh nilai Cosine Similarity sebesar 0.018474. Nilai tersebut sangat dekat dengan 0 sehingga menunjukkan bahwa arah vektor karakteristik CO dan CO₂ memiliki tingkat kemiripan yang sangat rendah.

Hasil analisis korelasi Pearson menunjukkan nilai sebesar 0.008837 dengan p-value sebesar 0.911976. Nilai korelasi yang sangat dekat dengan 0 menunjukkan bahwa hubungan linear antara output fitur CO dan CO₂ sangat lemah. Selain itu, nilai p-value yang lebih besar dari 0.05 menunjukkan bahwa tidak terdapat hubungan linear yang signifikan secara statistik pada tingkat signifikansi 5%.

Dengan demikian, berdasarkan representasi 68 jenis fitur TSFEL dan 159 output fitur yang memiliki nilai lengkap, karakteristik deret waktu CO dan CO₂ pada periode pengamatan yang sama tidak menunjukkan kemiripan yang kuat maupun hubungan linear yang signifikan.

## 10. Kesimpulan

Analisis data kualitas udara dilakukan terhadap Karbon Monoksida (CO) pada Kecamatan Gubeng, Kota Surabaya menggunakan data Sentinel-5P. Tahapan analisis meliputi pemahaman data, penentuan Area of Interest (AOI), pengambilan data, eksplorasi data, preprocessing, ekstraksi fitur menggunakan TSFEL, serta analisis kemiripan antara CO dan CO₂.

Pada tahap preprocessing, data CO diperiksa terhadap missing value dan outlier. Missing value ditangani menggunakan interpolasi linear yang dilengkapi dengan backward fill dan forward fill. Identifikasi outlier dilakukan menggunakan metode Interquartile Range (IQR), kemudian nilai outlier diperbaiki menggunakan interpolasi sehingga diperoleh deret waktu CO yang telah melalui proses pembersihan data.

Ekstraksi fitur menggunakan TSFEL dilakukan dengan 68 jenis fitur untuk memperoleh representasi karakteristik deret waktu CO. Hasil ekstraksi menghasilkan 164 output numerik karena beberapa jenis fitur dapat menghasilkan lebih dari satu output. Pendekatan yang sama diterapkan pada data CO₂ untuk memperoleh representasi fitur yang dapat dibandingkan.

Analisis kemiripan dilakukan pada periode ketika data CO dan CO₂ tersedia secara bersamaan. Data CO₂ yang memiliki resolusi pengamatan per menit diagregasi menjadi nilai rata-rata harian sehingga memiliki resolusi waktu yang sama dengan data CO. Setelah penyelarasan berdasarkan tanggal, diperoleh 102 hari pengamatan yang dapat dibandingkan.

Dari 68 jenis fitur TSFEL diperoleh 164 output numerik. Sebanyak 159 output fitur memiliki nilai lengkap pada kedua parameter dan digunakan dalam analisis kemiripan, sedangkan 5 output fitur tidak digunakan karena tidak dapat dihitung pada data CO₂ akibat keterbatasan jumlah titik data yang memenuhi persyaratan fitur tersebut.

Hasil Cosine Similarity antara vektor fitur CO dan CO₂ sebesar 0.018474. Nilai tersebut sangat dekat dengan 0 sehingga menunjukkan bahwa arah vektor karakteristik CO dan CO₂ memiliki tingkat kemiripan yang sangat rendah. Sementara itu, korelasi Pearson menghasilkan nilai sebesar 0.008837 dengan p-value sebesar 0.911976. Nilai korelasi yang sangat dekat dengan 0 menunjukkan hubungan linear yang sangat lemah, sedangkan p-value yang lebih besar dari 0.05 menunjukkan bahwa hubungan tersebut tidak signifikan secara statistik pada tingkat signifikansi 5%.

Berdasarkan keseluruhan hasil analisis, karakteristik deret waktu CO dan CO₂ pada periode pengamatan yang sama tidak menunjukkan kemiripan yang kuat berdasarkan representasi fitur TSFEL serta tidak menunjukkan hubungan linear yang signifikan secara statistik.
