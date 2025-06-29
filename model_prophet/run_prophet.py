import pandas as pd
import plotly.graph_objects as go
from prophet import Prophet
import os
import pickle
import streamlit as st

# -------- CONFIG --------
MODELOS_DIR = "model_prophet"
DATA_PATH = os.path.join("data", "temperaturas_limpias_10_años_sin_racha_clusters.pkl") # usá el temperatuas que tengas
ESTACIONES_PATH = os.path.join("data", "estaciones_nombre_indicativo.csv")

# -------- CARGA DE DATOS --------
@st.cache_data
def cargar_datos():
    df = pd.read_pickle(DATA_PATH)

    try:
        estaciones = pd.read_csv(ESTACIONES_PATH)
        required_cols = {"indicativo", "cluster", "nombre_indicativo"}
        if not required_cols.issubset(estaciones.columns):
            st.error("El archivo estaciones_nombre_indicativo.csv debe contener las columnas 'indicativo', 'cluster' y 'nombre_indicativo'.")
            st.stop()
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {ESTACIONES_PATH}")
        st.stop()

    if "cluster" not in df.columns or "nombre_indicativo" not in df.columns:
        st.warning("No se encontró 'cluster' o 'nombre_indicativo'. Intentando merge por 'indicativo'...")
        df = df.merge(estaciones[["indicativo", "cluster", "nombre_indicativo"]], on="indicativo", how="left")

        if df[["cluster", "nombre_indicativo"]].isna().any().any():
            st.error("Algunas estaciones no pudieron ser asociadas correctamente tras el merge.")
            st.stop()

    return df, estaciones

df, estaciones = cargar_datos()

# -------- SELECCIÓN DE ESTACIÓN --------
st.title("📈 Predicción de Temperatura por Estación")

# Crear diccionario: {nombre_legible: indicativo}
opciones_estaciones = dict(zip(estaciones["nombre_indicativo"], estaciones["indicativo"]))
nombre_seleccionado = st.selectbox("Selecciona una estación", list(opciones_estaciones.keys()))
indicativo = opciones_estaciones[nombre_seleccionado]

# -------- OBTENER CLUSTER Y FILTRAR DATOS --------
df_estacion = df[df["indicativo"] == indicativo]
if df_estacion.empty:
    st.warning("No hay datos para esta estación.")
    st.stop()

cluster = df_estacion["cluster"].iloc[0]
df_modelo = df_estacion[["fecha", "tmed"]].rename(columns={"fecha": "ds", "tmed": "y"}).dropna()

st.info(f"📍 Estación: {nombre_seleccionado} | Indicativo: {indicativo} | Cluster: {cluster}")

# -------- CARGA DEL MODELO DEL CLUSTER --------
@st.cache_resource
def load_model(cluster):
    path = os.path.join(MODELOS_DIR, f"cluster_model_{cluster}.pkl")
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_model(cluster)

# -------- PREDICCIÓN --------
st.subheader(f"🔮 Predicción de temperatura para: {nombre_seleccionado}")

periodos = [1, 7, 15, 30]
forecasts = {}

for periodo in periodos:
    future = model.make_future_dataframe(periods=periodo)
    forecast = model.predict(future)
    forecasts[periodo] = forecast

    # Mostrar predicciones tabulares
    st.write(f"**Pronóstico para {periodo} día(s):**")
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periodo))

    # Gráfico interactivo
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name="Pronóstico", line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], name="Límite superior", line=dict(color='lightblue'), fill=None))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], name="Límite inferior", line=dict(color='lightblue'), fill='tonexty'))
    fig.add_trace(go.Scatter(x=df_modelo['ds'], y=df_modelo['y'], name="Histórico", line=dict(color='black')))
    fig.update_layout(title=f"Pronóstico {periodo} días - {nombre_seleccionado}", xaxis_title="Fecha", yaxis_title="Temperatura media")
    st.plotly_chart(fig)
