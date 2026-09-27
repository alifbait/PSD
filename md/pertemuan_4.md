# Analisis K-Means Menggunakan PCA dan Tanpa PCA

Tugas pada pertemuan ini dilakukan untuk membandingkan hasil pengelompokan menggunakan metode K-Means tanpa PCA dan K-Means dengan PCA.

PCA (Principal Component Analysis) digunakan untuk menyederhanakan data dengan mengurangi jumlah variabel menjadi beberapa komponen utama tanpa menghilangkan informasi penting dari data.

## Workflow

Workflow yang digunakan terdiri dari beberapa proses, yaitu Excel Reader sebagai sumber data, K-Means untuk proses clustering tanpa PCA, Table View untuk melihat data, PCA untuk melakukan reduksi dimensi, serta K-Means dan Table View untuk menganalisis hasil setelah proses PCA.

![image.png](../img/07817958-e3ac-4777-86ea-58b62bc0480c.png)

## Table View Tanpa PCA

Pada tahap ini, data dari Excel Reader langsung diteruskan ke Table View untuk melihat struktur data sebelum dilakukan proses PCA. Data juga digunakan sebagai input untuk K-Means tanpa melalui proses reduksi dimensi.

![image.png](../img/9c3f12f4-20a0-4572-a0df-1734f764e1cb.png)

## Table View Dengan PCA

Pada tahap berikutnya, data dari Excel Reader diproses menggunakan PCA untuk melakukan reduksi dimensi. Hasil dari PCA kemudian diteruskan ke Table View untuk melihat data setelah dilakukan reduksi dimensi.

Pada hasil ini, jumlah variabel menjadi lebih sedikit dibandingkan data awal karena fitur-fitur asli direpresentasikan dalam bentuk komponen utama PCA.

![image.png](../img/d550e8d5-980b-4818-baed-05a65f1d23f7.png)

## Hasil K-Means Tanpa PCA

Pada tahap ini, K-Means digunakan secara langsung pada data asli tanpa melalui proses PCA. Hasil pengelompokan digunakan untuk melihat cluster yang terbentuk berdasarkan seluruh fitur yang tersedia pada data.

![image.png](../img/39ec2156-cdc0-4554-8790-8293fe133ffd.png)

## Hasil K-Means Dengan PCA

Pada tahap ini, K-Means digunakan pada data yang telah melalui proses reduksi dimensi menggunakan PCA. Hasil clustering kemudian dibandingkan dengan hasil K-Means tanpa PCA untuk melihat perbedaan pengelompokan setelah jumlah variabel direduksi.

![image.png](../img/996330d2-0d99-49b0-950d-6765661e2d30.png)

## Perbandingan Hasil

Perbandingan dilakukan antara hasil K-Means tanpa PCA dan hasil K-Means dengan PCA. K-Means tanpa PCA menggunakan fitur asli secara langsung, sedangkan K-Means dengan PCA menggunakan komponen utama hasil reduksi dimensi.

Perbandingan kedua hasil tersebut digunakan untuk melihat pengaruh penggunaan PCA terhadap proses pengelompokan data.
