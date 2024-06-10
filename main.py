import streamlit as st
import pandas as pd
import plotly.express as px

# Cargando los datos (simulado, reemplazar con las rutas correctas y ajustar la carga según tus archivos)
internet_usage = pd.read_csv('./datos/Individuals using the Internet (% of population).csv')
co2_emissions_total = pd.read_csv('./datos/CO2 emissions (kt).csv')
population_growth = pd.read_csv('./datos/Population growth (annual %).csv')
co2_emissions_electricity_heat = pd.read_csv('./datos/CO2 emissions from electricity and heat production, total (% of total fuel combustion).csv')
carbon_intensity = pd.read_csv('./datos/carbon_intensity.csv')
power_consumption = pd.read_csv('./datos/power_breakdown.csv')
# Configuración de la página

def add_center_image_inline_with_circular_border(url):
    st.markdown(
        f"""
        <style>
        .img-container {{
            display: flex;
            justify-content: center;
            padding: 20px;
        }}
        .circular--portrait {{
            border-radius: 50%;
            width: 50%;
            height: 50%;
        }}
        </style>
        <div class="img-container">
            <img src="{url}" class="circular--portrait"/>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_data_info():
    st.sidebar.header("Transparencia de los datos")
    dataset = st.sidebar.selectbox("Seleccione los datos para ver detalles:",
                                   ("Uso de Internet", "Emisiones Totales de CO2", "Crecimiento de la Población", "Emisiones de CO2 de Electricidad y Calor", "Intensidad de Carbono", "Consumo Energético"))
    
    if dataset == "Uso de Internet":
        st.sidebar.write("""
        **Uso de Internet (% de la población)**
        - **Descripción**: Representa el porcentaje de personas que utilizan Internet en cada país.
        - **Fuente**: World Bank - World Development Indicators
        - **URL**: [World Development Indicators](https://github.com/open-numbers/ddf--open_numbers--world_development_indicators)
        """)
        
    elif dataset == "Emisiones Totales de CO2":
        st.sidebar.write("""
        **Emisiones Totales de CO2 (kt)**
        - **Descripción**: Muestra las emisiones totales de dióxido de carbono en kilotoneladas, reflejando el impacto ambiental.
        - **Fuente**: World Bank - World Development Indicators
        - **URL**: [World Development Indicators](https://github.com/open-numbers/ddf--open_numbers--world_development_indicators)
        """)
        
    elif dataset == "Crecimiento de la Población":
        st.sidebar.write("""
        **Crecimiento de la Población (% anual)**
        - **Descripción**: Tasa de crecimiento poblacional anual por país.
        - **Fuente**: World Bank - World Development Indicators
        - **URL**: [World Development Indicators](https://github.com/open-numbers/ddf--open_numbers--world_development_indicators)
        """)
        
    elif dataset == "Emisiones de CO2 de Electricidad y Calor":
        st.sidebar.write("""
        **Emisiones de CO2 de la Producción de Electricidad y Calor (% del total de combustión de combustible)**
        - **Descripción**: Porcentaje de emisiones de CO2 provenientes de la producción de electricidad y calor respecto al total de la combustión de combustible en cada país.
        - **Fuente**: World Bank - World Development Indicators
        - **URL**: [World Development Indicators](https://github.com/open-numbers/ddf--open_numbers--world_development_indicators)
        """)
    elif dataset == "Intensidad de Carbono":
        st.sidebar.markdown("""
        **Intensidad de Carbono en gCO2eq/kWh por país**
        - **Descripción**: Intensidad de las emisiones de carbono por cada kWh de electricidad producida, reflejando la sostenibilidad de las fuentes de energía.
        - **Fuente**: Electricity Map API.
        """)
    
    elif dataset == "Consumo Energético":
        st.sidebar.markdown("""
        **Consumo Energético**
        - **Descripción**: Desglose del consumo energético por tipo de fuente en MW, proporcionando una visión del mix energético de una región.
        - **Fuente**: Electricity Map API.
        """)
st.set_page_config(page_title='Digitopía Sustentable: Visualizando el Futuro Ecológico de la Era Digital', layout='wide')
display_data_info()
st.title('Impacto Digital en la Transición Ecológica')
st.markdown("""
    <style>
    .stActionButton {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

add_center_image_inline_with_circular_border("https://sostenibles.org/wp-content/uploads/2021/03/numerique-et-environement-1024x717.jpg")
st.markdown("""
Esta aplicación explora la interacción entre el uso digital y la transición ecológica a través de datos globales.
Seleccione diferentes métricas para ver cómo varían geográficamente y en relación con otros indicadores.
""")

# Selector de tipo de datos para visualización en mapa
data_options = st.selectbox(
    'Seleccione el tipo de dato a visualizar:',
    ('Uso de Internet', 'Emisiones de CO2 Totales', 'Crecimiento de la Población', 'Emisiones de CO2 de Electricidad y Calor', 'Intensidad de Carbono')
)

def create_map(data, column):
    fig = px.choropleth(data, locations="Country", color=column, hover_name="Country", locationmode='country names', color_continuous_scale='Viridis', title=column, animation_frame= 'Year')
    return fig

if data_options == 'Uso de Internet':
    st.plotly_chart(create_map(internet_usage, 'Uso de Internet (% de la población)'))
elif data_options == 'Emisiones de CO2 Totales':
    st.plotly_chart(create_map(co2_emissions_total, 'Emisiones de CO2 (kt)'))
elif data_options == 'Crecimiento de la Población':
    st.plotly_chart(create_map(population_growth, 'Crecimiento demográfico (anual %)'))
elif data_options == 'Emisiones de CO2 de Electricidad y Calor':
    fig_co2_electricity = create_map(co2_emissions_electricity_heat, 'Emisiones de CO2 procedentes de la producción de electricidad y calor, total (% de la combustión total)')
    # update legend name 
    fig_co2_electricity.update_layout(coloraxis_colorbar=dict(title='Emisiones de CO2 (%)'))
    st.plotly_chart(fig_co2_electricity)
elif data_options == 'Intensidad de Carbono':
    fig = px.choropleth(carbon_intensity, locations="Country_x", locationmode='country names', color="carbonIntensity", hover_name="zone", color_continuous_scale="Viridis", title="Intensidad de carbono en gCO2eq/kWh por país en tiempo real")
    st.plotly_chart(fig)

# Análisis por país del consumo energético
st.header("Análisis por País del Consumo Energético en tiempo real")
st.write("Seleccione un país para ver el desglose del consumo energético por tipo de fuente en MW.")
country_select = st.selectbox('Seleccione un país:', power_consumption['Country'].unique())
country_data = power_consumption[power_consumption['Country'] == country_select]

fig = px.bar(country_data, x='zone', y=[col for col in country_data.columns if col not in ['zone', 'datetime', 'ISO_CODE', 'Country', 'Zone']], title=f'Consumo Energético en {country_select}', labels={'value': 'Consumo (MW)', 'variable': 'Tipo de Energía'})
st.plotly_chart(fig)