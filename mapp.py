import pandas as pd
import folium

# Carregar os dados
idhm = pd.read_excel("indicadores.xlsx")

# URL do GeoJSON
geojson_url = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-24-mun.json"

# Mapa inicial
mapa_idhm_rn = folium.Map([-5.93009349109802, -35.60928289352865],
                         tiles="cartodbpositron",
                         zoom_start=8)

# Criando o mapa coroplético
folium.Choropleth(
    geo_data=geojson_url,
    data=idhm,
    columns=["Mun", "IDSF"],
    key_on="feature.properties.name",
    fill_color="GnBu",
    fill_opacity=0.9,
    line_opacity=0.5,
    legend_name="IDSF",
    nan_fill_color="white",
    name="Dados"
).add_to(mapa_idhm_rn)

# Adicionando a função de destaque
estilo = lambda x: {"fillColor": "white",
                   "color": "black",
                   "fillOpacity": 0.001,
                   "weight": 0.001}

estilo_destaque = lambda x: {"fillColor": "darkblue",
                            "color": "black",
                            "fillOpacity": 0.5,
                            "weight": 1}

highlight = folium.features.GeoJson(
    data=geojson_url,
    style_function=estilo,
    highlight_function=estilo_destaque,
    name="Destaque"
)

# Adicionando caixa de texto
folium.features.GeoJsonTooltip(
    fields=["name"],
    aliases=["Mun"],
    labels=False,
    style=("background-color: white; color: black; font-family: arial; font-size: 16px; padding: 10px;")
).add_to(highlight)

# Adicionando o destaque ao mapa
mapa_idhm_rn.add_child(highlight)

# Adicionando o controle de camadas
folium.LayerControl().add_to(mapa_idhm_rn)

# Salvando o mapa em um arquivo HTML
mapa_idhm_rn.save("mapa_idhm_rn.html")
