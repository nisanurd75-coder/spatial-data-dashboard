import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Mekânsal Veri Dashboard",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ GeoJSON / KML Veri Analiz ve Görüntüleme Paneli")
st.write("Mekânsal dosyalarınızı yükleyin, haritada inceleyin ve otomatik metrik hesaplamalarını görün.")

# Sol Yan Menü - Dosya Yükleme
st.sidebar.header("📂 Dosya Yükleme")
uploaded_file = st.sidebar.file_uploader(
    "GeoJSON veya KML dosyası yükleyin", 
    type=["geojson", "json", "kml"]
)

if uploaded_file is not None:
    try:
        # GeoPandas ile dosyayı okuma
        gdf = gpd.read_file(uploaded_file)
        
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)
            
        st.sidebar.success("Dosya başarıyla yüklendi!")

        # -------------------------------------------------------------
        # METRİK HESAPLAMALARI (Alan ve Uzunluk)
        # -------------------------------------------------------------
        # Metrik hesaplama için EPSG:3857 (Web Mercator) projeksiyonuna dönüştürme
        gdf_projected = gdf.to_crs(epsg=3857)
        
        gdf['Alan (m²)'] = gdf_projected.geometry.area
        gdf['Alan (Hektar)'] = gdf['Alan (m²)'] / 10000
        gdf['Uzunluk/Çevre (m)'] = gdf_projected.geometry.length

        # -------------------------------------------------------------
        # HARİTA GÖRSELLEŞTİRME (Açık Katman Kullanımı)
        # -------------------------------------------------------------
        centroid = gdf.to_crs(epsg=4326).unary_union.centroid
        # CartoDB yerine OpenStreetMap katmanı kullanarak API Key uyarısını kaldırıyoruz
        m = folium.Map(location=[centroid.y, centroid.x], zoom_start=14, tiles="OpenStreetMap")

        folium.GeoJson(
            gdf,
            name="Yüklenen Veri",
            style_function=lambda x: {
                'fillColor': '#3186cc',
                'color': '#2b8cbe',
                'weight': 3,
                'fillOpacity': 0.4
            }
        ).add_to(m)

        st.subheader("📍 İnteraktif Harita")
        st_folium(m, width=1000, height=500)

        # -------------------------------------------------------------
        # ÖZET İSTATİSTİKLER VE TABLO
        # -------------------------------------------------------------
        st.subheader("📊 Metrik Hesaplamaları ve Öznitelik Tablosu")
        
        # Metrik Kartları
        col1, col2, col3 = st.columns(3)
        col1.metric("Obje Sayısı", len(gdf))
        col2.metric("Toplam Alan", f"{gdf['Alan (Hektar)'].sum():.2f} ha")
        col3.metric("Toplam Uzunluk / Çevre", f"{gdf['Uzunluk/Çevre (m)'].sum():.2f} m")

        # Geometri kolonunu gizleyip tabloyu göster
        display_df = gdf.drop(columns=['geometry'])
        st.dataframe(display_df, use_container_width=True)

    except Exception as e:
        st.error(f"Dosya işlenirken hata oluştu: {e}")
else:
    st.info("💡 Başlamak için sol taraftaki menüden bir GeoJSON veya KML dosyası yükleyin.")