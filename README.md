<img width="1917" height="972" alt="Ekran görüntüsü 2026-09-09 000503" src="https://github.com/user-attachments/assets/1815451d-6d67-408c-a0d1-9ed7f6664627" />
# 🗺️ Spatial Data Analysis & Web GIS Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![GeoPandas](https://img.shields.io/badge/GeoPandas-0.14+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, Harita Mühendisliği ve Mekânsal Veri Analitiği süreçlerini otomatikleştirmek, GIS (CBS) verilerini web ortamında görselleştirmek ve etkileşimli analizler gerçekleştirmek amacıyla geliştirilmiş profesyonel bir Web GIS uygulamasıdır.

🔗 **Canlı Demo (Live App):** [spatial-data-dashboard-nisanur.streamlit.app](https://spatial-data-dashboard-nisanur.streamlit.app/)

---

## 🌟 Öne Çıkan Özellikler

- 📂 **Çoklu Vektör Format Desteği:** `GeoJSON` ve `KML` formatındaki mekânsal veri dosyalarını yükleme, haritada işleme ve görselleştirme.
- 📐 **Otomatik Metrik Hesaplama:** Yüklenen veya çizilen poligonlar için Hektar ve m² cinsinden dinamik alan; çizgiler için metre cinsinden çevre ve uzunluk hesabı.
- 📊 **Dinamik Karşılaştırma & Öznitelik Tablosu:** Yüklenen katmanlar ile harita üzerinde anlık çizilen geometrileri eşzamanlı olarak tek bir tabloda birleştirme, listeleme ve karşılaştırma.
- 🗺️ **Çeşitli Altlık Haritalar (Layer Control):** OpenStreetMap, Esri World Imagery (Uydu Görüntüsü) ve OpenTopoMap (Topoğrafik Harita) katmanları arasında tek tıkla geçiş.
- ✏️ **Gelişmiş Çizim & Düzenleme Araçları:** Harita üzerinde poligon, çizgi, dikdörtgen ve nokta çizimi; çizilen objeleri tekli silme ve nodlar üzerinden geometrik düzenleme.
- 📍 **Anlık WGS84 Koordinat Takibi:** Harita üzerinde imlecin bulunduğu noktanın dinamik WGS84 (Enlem/Boylam) koordinat akışı ve geometrilerin otomatik merkez (centroid) tespiti.
- 📥 **Veri Dışa Aktarımı (Export):** Hesaplanan sözel ve mekânsal öznitelik verilerini tek tıkla `.csv` formatında bilgisayara indirme.

---

## 🛠️ Teknolojik Mimari ve Kütüphaneler

| Alan | Kullanılan Teknoloji / Kütüphane |
| :--- | :--- |
| **Programlama Dili** | Python 3.10+ |
| **Web Framework** | Streamlit |
| **Mekânsal Veri İşleme** | GeoPandas, Shapely, PyProj |
| **Haritacılık & Etkileşim** | Folium, Streamlit-Folium |
| **Veri Analizi & Tablo** | Pandas, NumPy |

---

## 🚀 Yerelde Çalıştırma Rehberi

Projeyi kendi bilgisayarınızda klonlayıp çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1. Repoyu Klonlayın
git clone [https://github.com/nisanurd75-coder/spatial-data-dashboard.git](https://github.com/nisanurd75-coder/spatial-data-dashboard.git)
cd spatial-data-dashboard

2. Gerekli Kütüphaneleri Yükleyin
pip install -r requirements.txt

3. Uygulamayı Başlatın
streamlit run app.py

## ** 📸 Uygulama Ekran Görüntüleri & Kullanım

1.Dosya Yükleme: Sol yan menüden GeoJSON/KML dosyanızı sürükleyip bırakın.

2.Çizim & Ölçüm: Sol üstteki çizim araçlarını kullanarak haritaya yeni alanlar veya rotalar ekleyin.

3.Tekli Silme: Çöp kutusu simgesine tıklayıp silmek istediğiniz objeyi seçin ve Save butonuna basın.

4.CSV İndirme: Tablonun altındaki indirme butonunu kullanarak hesaplama sonuçlarını dışa aktarın.

📜 Lisans
Bu proje MIT Lisansı altında korunmaktadır. İstediğiniz gibi geliştirebilir ve kullanabilirsiniz.
