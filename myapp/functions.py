import requests
import pandas as pd
from io import BytesIO
import plotly.graph_objs as go
import traceback

from datetime import datetime
import threading

# URL del archivo en OneDrive
ONEDRIVE_URL = "https://immaipu-my.sharepoint.com/personal/karen_arancibia_maipu_cl/_layouts/15/download.aspx?share=Ec0mjRB4LrtCowyUYI11QVEBQ-XnXwoR48kodbA5qBUprg"

# Caché de datos global
df_cache = None
ultima_actualizacion = None

def descargar_datos():
    """Descarga y carga los datos en un DataFrame global."""
    global df_cache, ultima_actualizacion
    try:
        inicio = datetime.now()

        response = requests.get(ONEDRIVE_URL, stream=True, timeout=10)
        response.raise_for_status()

        # Cargar solo columnas necesarias con tipos optimizados
        df = pd.read_excel(BytesIO(response.content),                           
                            # Ajustar según sea necesario
                           engine="openpyxl")
        
        df["Dif registro"] = pd.to_datetime(df["Dif registro"], dayfirst=True, errors="coerce")

        df_cache = df
        ultima_actualizacion = datetime.now()
        
        print(f"📥 Archivo actualizado en {ultima_actualizacion}, tomó {ultima_actualizacion - inicio} segundos")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error al descargar el archivo: {e}")
    except Exception as e:
        print(f"⚠️ Error al procesar el archivo: {e}")

def cargar_datos():
    """Devuelve el DataFrame en caché, o lo descarga si no existe."""
    if df_cache is None:
        descargar_datos()
    return df_cache

def actualizar_cada_x_segundos(intervalo=60*10):
    """Descarga automáticamente los datos cada cierto tiempo (en segundos)."""
    descargar_datos()
    threading.Timer(intervalo, actualizar_cada_x_segundos, [intervalo]).start()
    print("descargado")

# Llamar esta función al iniciar la app en Django
actualizar_cada_x_segundos()

# Función para crear el gráfico del botón
def crear_boton(df, columna, es_verde, columna_caudal):
    try:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")
        print(df[columna_caudal])
        ultimo_valor = df[columna].iloc[-1]
        color = 'green' if es_verde == ultimo_valor else ('#FFF302' if ultimo_valor == 'No (Detenido)' else 'red')
        ultimo_valor_caudal = df[columna_caudal].iloc[-1] if not columna_caudal==False else None
        anotation_text = f"Caudal: {ultimo_valor_caudal} l/s " if not pd.isna(ultimo_valor_caudal) else "Sin información disponible"
        
        fig = go.Figure(
            data=go.Scatter(
                x=[ultimo_valor],
                y=[0],
                mode='markers',
                marker=dict(color=color, size=100),
                name=f"Botón {'Verde' if es_verde else 'Rojo'}"
            )
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title=columna),
            yaxis=dict(title='', visible=False),
            showlegend=False,
            annotations=[dict(x=ultimo_valor, y=-0.05, text=anotation_text, showarrow=False, font=dict(size=12, color="black"))],
            height=400,
            width=300,
        )
        
        return fig.to_html(full_html=False, config={'displayModeBar': False})
    except Exception as e:
        print(f"Error al crear el gráfico: {e}")
        print(traceback.format_exc())
        return None
