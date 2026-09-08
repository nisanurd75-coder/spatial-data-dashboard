import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from folium.plugins import Draw, MousePosition
from streamlit_folium import st_folium
from shapely.geometry import shape

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Mekânsal Veri Dashboard",
    page_icon="🗺️",
    layout="wide"
)

st.title("🗺️ GeoJSON / KML Veri Analiz ve Görüntüleme Paneli")
st.write("Mekânsal dosyalarınızı yükleyin, ekranda yeni alanlar çizin ve karşılaştırmalı analiz yapın.")

# Sol Yan Menü - Dosya Yükleme
st.sidebar.header("📂 Dosya Yükleme")
uploaded_file = st.sidebar.file_uploader(
    "GeoJSON veya KML dosyası yükleyin", 
    type=["geojson", "json", "kml"]
)

map_center = [39.9334, 32.8597]
zoom_level = 6
features_list = []

# 1. Yüklenen Dosyayı İşleme
if uploaded_file is not None:
    try:
        gdf = gpd.read_file(uploaded_file)
        if gdf.crs is None:
            gdf = gdf.set_crs(epsg=4326)
            
        st.sidebar.success("Dosya başarıyla yüklendi!")

        for idx, row in gdf.iterrows():
            features_list.append({
                "Katman / Kaynak": f"Yüklenen Veri (Obje {idx+1})",
                "geometry": row.geometry
            })

        centroid = gdf.to_crs(epsg=4326).unary_union.centroid
        map_center = [centroid.y, centroid.x]
        zoom_level = 14

    except Exception as e:
        st.error(f"Dosya işlenirken hata oluştu: {e}")

# -------------------------------------------------------------
# HARİTA VE ALTLIKLAR
# -------------------------------------------------------------
m = folium.Map(location=map_center, zoom_start=zoom_level, tiles="OpenStreetMap", name="OpenStreetMap")

# Altlık Katmanları (max_zoom eklendi, böylece max zoom hatası vermez)
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Uydu Görüntüsü (Esri)',
    max_zoom=19
).add_to(m)

folium.TileLayer(
    tiles='https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    attr='OpenTopoMap',
    name='Topoğrafik Harita',
    max_zoom=17
).add_to(m)

# Çizim Aracı (Draw)
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
    },
    edit_options={
        "edit": True,      # Çizilen objelerin köşelerinden çekip şeklini değiştirmeyi sağlar
        "remove": True     # Tekli silme modunu aktif eder
    }
).add_to(m)

# 🌐 BELİRGİN KOORDİNAT GÖSTERGESİ (WGS84 Enlem / Boylam)
formatter = "function(num) {return L.Util.formatNum(num, 5) + '°';};"
MousePosition(
    position="bottomright",
    separator=" | Boylam: ",
    empty_string="Harita dışı",
    lng_first=False,
    num_digits=5,
    prefix="📍 Enlem: ",
    lat_formatter=formatter,
    lng_formatter=formatter
).add_to(m)

if uploaded_file is not None and len(features_list) > 0:
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

folium.LayerControl(position='topright').add_to(m)

st.subheader("📍 İnteraktif Harita")
st.info("💡 **Kullanım İpucu:** Çizimleri tekli silmek için sol üstteki **Çöp Kutusu** ikonuna tıklayın, silinecek objeyi seçip **Save** butonuna basın.")
map_data = st_folium(m, use_container_width=True, height=500, key="gis_map")

# 2. Harita Üzerinde Çizilen Yeni Objeleri Yakalama
if map_data and map_data.get("all_drawings"):
    drawings = map_data["all_drawings"]
    for idx, draw in enumerate(drawings):
        geom = shape(draw["geometry"])
        features_list.append({
            "Katman / Kaynak": f"Yeni Çizim {idx+1}",
            "geometry": geom
        })

# -------------------------------------------------------------
# DİNAMİK METRİK HESAPLARI VE TABLO
# -------------------------------------------------------------
if len(features_list) > 0:
    full_gdf = gpd.GeoDataFrame(features_list, crs="EPSG:4326")
    
    # Metrik Projeksiyonda (EPSG:3857) Alan ve Uzunluk Hesabı
    full_gdf_proj = full_gdf.to_crs(epsg=3857)
    full_gdf['Alan (m²)'] = full_gdf_proj.geometry.area
    full_gdf['Alan (Hektar)'] = full_gdf['Alan (m²)'] / 10000
    full_gdf['Uzunluk / Çevre (m)'] = full_gdf_proj.geometry.length

    # WGS84 Merkez Koordinatlarını Tabloya Ekleme (Enlem/Boylam)
    full_gdf['Merkez Enlem (WGS84)'] = full_gdf.geometry.centroid.y
    full_gdf['Merkez Boylam (WGS84)'] = full_gdf.geometry.centroid.x

    st.subheader("📊 Dinamik Öznitelik ve Karşılaştırma Tablosu")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Toplam Obje Sayısı", len(full_gdf))
    col2.metric("Toplam Alan", f"{full_gdf['Alan (Hektar)'].sum():.2f} ha")
    col3.metric("Toplam Uzunluk / Çevre", f"{full_gdf['Uzunluk / Çevre (m)'].sum():.2f} m")

    display_df = full_gdf.drop(columns=['geometry'])
    st.dataframe(display_df, use_container_width=True)

    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Tüm Analiz Sonuçlarını CSV Olarak İndir",
        data=csv_data,
        file_name="dinamik_mekansal_analiz.csv",
        mime="text/csv"
    )
else:
    st.info("💡 Başlamak için bir dosya yükleyin veya harita üzerindeki araçları kullanarak çizim yapın.")