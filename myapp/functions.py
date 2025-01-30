import requests
import pandas as pd
from io import BytesIO
import plotly.graph_objs as go
import traceback

# Función para descargar y cargar los datos
def cargar_datos(onedrive_url):
    try:
        response = requests.get(onedrive_url)
        response.raise_for_status()  # Verifica errores en la descarga
        df = pd.read_excel(BytesIO(response.content))
        df['Dif registro'] = pd.to_datetime(df['Dif registro'], dayfirst=True, format='mixed')
        
        return df
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar el archivo: {e}")
        return None
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None

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
