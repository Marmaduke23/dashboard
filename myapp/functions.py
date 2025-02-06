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
    t=threading.Timer(intervalo, actualizar_cada_x_segundos, [intervalo])
    t.daemon=True
    t.start()
    print("descargado")

# Llamar esta función al iniciar la app en Django
actualizar_cada_x_segundos()

# Función para crear el gráfico del botón
def crear_boton(df, columna, es_verde, columna_caudal):
    try:
        if columna not in df.columns:
            raise ValueError(f"La columna '{columna}' no existe en el DataFrame.")
        ultimo_valor = df[columna].iloc[-1]
        color = 'green' if es_verde == ultimo_valor else ('#FFF302' if ultimo_valor == 'No (Detenido)' else 'red')
        ultimo_valor_caudal = df[columna_caudal].iloc[-1] if not columna_caudal==False else None
        anotation_text = f"Caudal: {ultimo_valor_caudal} l/s " if not pd.isna(ultimo_valor_caudal) else "Caudal: Sin información"
        
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
        xaxis=dict(title=columna,title_standoff=5),
        yaxis=dict(title='', visible=False,range=[-1, 1]),
        showlegend=False,
        annotations=[dict(x=ultimo_valor, y=-0.5, text=anotation_text, showarrow=False, font=dict(size=12))],
        autosize=True,  # Hace que el tamaño se ajuste automáticamente
        margin=dict(l=20, r=20, t=20, b=20),  # Ajusta los márgenes para evitar recortes
    )
        
        return fig.to_html(full_html=False, config={'displayModeBar': False})
    except Exception as e:
        print(f"Error al crear el gráfico: {e}")
        print(traceback.format_exc())
        return None


import plotly.graph_objects as go
import pandas as pd

def generar_grafico_estanque(nivel_maximo, nivel_actual, estanque, unidad, rm=0, rb=0):
    """
    Genera un gráfico estilo "estanque" que muestra el nivel máximo y el nivel actual de agua.

    Args:
        nivel_maximo (float): Nivel máximo del estanque en metros.
        nivel_actual (float): Nivel actual del estanque en metros.
        estanque (string): Nombre del estanque.
        unidad (string): Unidad de medida del nivel.
        rm (int): Rango medio desde cual el proyecto es amarillo.
        rb (int): Rango bajo desde cual el proyecto es rojo

    Returns:
        plotly.graph_objects.Figure: Gráfico del estanque.
    """
    color_agua = 'lightblue'
    # Definir color agua
    if nivel_actual <= rm and nivel_actual > rb:
        color_agua = 'yellow'
    elif nivel_actual < rb:
        color_agua = 'red'

    # Crear la figura
    fig = go.Figure()

    # Agregar la barra del contenedor del estanque (nivel máximo)
    fig.add_trace(go.Bar(
        x=["Estanque"],
        y=[nivel_maximo],  # Altura máxima
        marker=dict(
            color='lightgrey',  # Fondo del estanque
            line=dict(color='lightgrey', width=10)  # Bordes del estanque
        ),
        hoverinfo='none',  # Sin información al pasar el mouse
        name="Capacidad Máxima",
        width=0.7  # Aumentar el grosor de la barra
    ))

    # Agregar la barra del nivel actual (agua dentro del estanque)
    fig.add_trace(go.Bar(
        x=["Estanque"],
        y=[nivel_actual],  # Nivel actual de agua
        marker=dict(color=color_agua),  # Color del agua
        hovertemplate=f"Nivel Actual: {nivel_actual:.2f} m",  # Mostrar el nivel actual en metros
        name="Nivel Actual",
        width=0.7  # Aumentar el grosor de la barra
    ))

    # Ajustar el diseño para que parezca un estanque
    fig.update_layout(
        title=f"Nivel del Estanque {estanque}",
        barmode='overlay',  # Superponer barras
        yaxis=dict(
            title=f"Nivel [{unidad}]",
            range=[0, nivel_maximo],  # Rango desde 0 hasta el máximo
            showgrid=False,  # Sin líneas de la cuadrícula
            ticksuffix=f" {unidad}"  # Sufijo para mostrar unidades en el eje
        ),
        xaxis=dict(
            showticklabels=False  # Sin etiquetas en el eje X
        ),
        plot_bgcolor="rgba(0,0,0,0)",  # Fondo transparente
        height=500,  # Altura del gráfico
        showlegend=False,  # Ocultar leyenda
        margin=dict(t=60),  # Aumentar margen superior (espacio entre título y gráfico)
    )

    return fig.to_html(full_html=False, config={'displayModeBar': False})

