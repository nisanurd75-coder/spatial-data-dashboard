import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Mekânsal Veri Dashboard",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ GeoJSON / KML Veri Analiz ve Görüntüleme Paneli")
st.write("Mekânsal dosyalarınızı yükleyin, haritada inceleyin, çizim yapın ve analiz sonuçlarını indirin.")

# Sol Yan Menü - Dosya Yükleme
st.sidebar.header("📂 Dosya Yükleme")
uploaded_file = st.sidebar.file_uploader(
    "GeoJSON veya KML dosyası yükleyin", 
    type=["geojson", "json", "kml"]
)

map_center = [39.9334, 32.8597]
zoom_level = 6

if uploaded_file is not None:
    try:
        gdf = gpd.read_file(uploaded_file)
        
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)
            
        st.sidebar.success("Dosya başarıyla yüklendi!")

        # Metrik Hesaplamaları
        gdf_projected = gdf.to_crs(epsg=3857)
        gdf['Alan (m²)'] = gdf_projected.geometry.area
        gdf['Alan (Hektar)'] = gdf['Alan (m²)'] / 10000
        gdf['Uzunluk/Çevre (m)'] = gdf_projected.geometry.length

        # Harita merkezini verinin ortasına odakla
        centroid = gdf.to_crs(epsg=4326).unary_union.centroid
        map_center = [centroid.y, centroid.x]
        zoom_level = 14

    except Exception as e:
        st.error(f"Dosya işlenirken hata oluştu: {e}")
        gdf = None
else:
    gdf = None
    st.info("💡 Başlamak için sol taraftaki menüden bir GeoJSON veya KML dosyası yükleyin.")

# -------------------------------------------------------------
# HARİTA, ALTLIKLAR, ÇİZİM ARAÇLARI VE KOORDİNAT BİLGİSİ
# -------------------------------------------------------------
m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="OpenStreetMap", name="OpenStreetMap")

# 1. Farklı Altlık Haritalar
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Uydu Görüntüsü (Esri)'
).add_to(m)

folium.TileLayer(
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr='OpenTopoMap',
    name='Topoğrafik Harita'
).add_to(m)

# 2. Çizim ve Ölçüm Araçları (Draw Control)
Draw(
    export=True,
    filename="cizim_verisi.geojson",
    position="topleft",
    draw_options={
        "polyline": True,
        "polygon": True,
        "rectangle": True,
        "circle": False,
        "marker": True,
        "circlemarker": False
    }
).add_to(m)

# 3. Anlık Koordinat Göstergesi (Mouse Position)
folium.LatLngPopup().add_to(m)

# Eğer dosya yüklendiyse GeoJSON'ı ekle
if gdf is not None:
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

# Katman Kontrol Menüsü (Sağ Üst)
folium.LayerControl(position='topright').add_to(m)

# Haritayı Ekrana Sığacak Şekilde Göster (use_container_width=True sağa taşmayı engeller)
st.subheader("📍 İnteraktif Harita")
st_folium(m, use_container_width=True, height=500)

# -------------------------------------------------------------
# METRİKLER, TABLO VE VERİ DIŞA AKTARMA (CSV DOWNLOAD)
# -------------------------------------------------------------
if gdf is not None:
    st.subheader("📊 Metrik Hesaplamaları ve Öznitelik Tablosu")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Obje Sayısı", len(gdf))
    col2.metric("Toplam Alan", f"{gdf['Alan (Hektar)'].sum():.2f} ha")
    col3.metric("Toplam Uzunluk / Çevre", f"{gdf['Uzunluk/Çevre (m)'].sum():.2f} m")

    display_df = gdf.drop(columns=['geometry'])
    st.dataframe(display_df, use_container_width=True)

    # 4. Veri Dışa Aktarma Butonu (CSV İndir)
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Tabloyu ve Hesaplamaları CSV Olarak İndir",
        data=csv_data,
        file_name="mekansal_analiz_sonuclari.csv",
        mime="text/csv"
    )