from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse  # Importa HttpResponse para enviar texto como respuesta
from django.http import JsonResponse
from .functions import cargar_datos, crear_boton, generar_grafico_estanque
import json
import pyodbc

@login_required 
def home(request):
    return render(request, 'home.html')  # Respuesta para la ruta '/'

def about(request):
    return render(request, 'about.html')   # Respuesta para la ruta '/about'

from django.http import JsonResponse
import random

@login_required 
def dashboard(request):
    """Renderiza la página del dashboard."""
    return render(request, "dashboard.html")




# URL de descarga
onedrive_url = "https://immaipu-my.sharepoint.com/personal/karen_arancibia_maipu_cl/_layouts/15/download.aspx?share=Ec0mjRB4LrtCowyUYI11QVEBQ-XnXwoR48kodbA5qBUprg"
import time
# Vista para actualizar el dashboard
def actualizar_dashboard(request):
    tiempos = {}
    inicio_carga = time.time()
    df = cargar_datos()
    print("tiempo de carga",time.time() - inicio_carga)
    
    if df is not None:
        boton_1a = crear_boton(df, 'Pozo 1A - Funcionamiento', 'Sí', 'Pozo 1A - Caudal l/s')
        boton_2a = crear_boton(df, 'Pozo 2A - Funcionamiento', 'Sí', 'Pozo 2A - Caudal l/s')
        boton_3a = crear_boton(df, 'Pozo 3A - Funcionamiento', 'Sí', 'Pozo 3A - Caudal l/s')
        boton_4a = crear_boton(df, 'Pozo 4A - Funcionamiento', 'Sí', 'Pozo 4A - Caudal l/s')
        boton_5 = crear_boton(df, 'Pozo 5 - Funcionamiento', 'Sí', 'Pozo 5 - Caudal l/s')
        boton_booster1=crear_boton(df, 'Booster 1 - Funcionamiento', 'Sí', False)
        boton_booster2=crear_boton(df, 'Booster 2 - Funcionamiento', 'Sí', False)
        boton_booster3=crear_boton(df, 'Booster 3 - Funcionamiento', 'Sí', False)
        boton_booster4=crear_boton(df, 'Booster 4 - Funcionamiento', 'Sí', False)
        boton_booster5=crear_boton(df, 'Booster 5 - Funcionamiento', 'Sí', False)
        graficoEstanque3000= generar_grafico_estanque(3000, df['Elevado 3000 m3 - Nivel de Estanque - m3'].iloc[-1],'elevado 3000','m3',1200,600)#cambiar volumen por altura
        graficoEstanque6000= generar_grafico_estanque(9, df['Semi Enterrado 6000 m3 - Nivel de Estanque - m'].iloc[-1],'semi enterrado 6000','m',3.5,1.7)#cambiar volumen por altura
        print("tiempo_boton",time.time() - inicio_carga)
        
        return JsonResponse({
            'botonPozo1A': boton_1a,
            'botonPozo2A': boton_2a,
            'botonPozo3A': boton_3a,
            'botonPozo4A': boton_4a,
            'botonPozo5': boton_5,
            'botonBooster1': boton_booster1,
            'botonBooster2': boton_booster2,
            'botonBooster3': boton_booster3,
            'botonBooster4': boton_booster4,
            'botonBooster5': boton_booster5,
            'graficoEstanque3000': graficoEstanque3000,
            'graficoEstanque6000': graficoEstanque6000,

        })
    else:
        return JsonResponse({'error': 'No se pudieron cargar los datos'}, status=500)

def obtener_datos(request):
    drivers = pyodbc.drivers()
    #print(pyodbc.drivers())
    # Definir la cadena de conexión (ajusta estos valores)
    server = '172DPRESIONES\\MSSQL2014'  # Dirección del servidor
    database = 'nombre_base_datos'      # Nombre de la base de datos
    username = 'consultaPresiones'      # Tu usuario
    password = 'conPres025'                    # Tu contraseña

    # Conectar a SQL Server usando pyodbc
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};'
                        f'SERVER={server};'
                        f'UID={username};'
                        f'PWD={password};'
                        f'TrustServerCertificate=yes;')


    # Consulta SQL para obtener el último valor de cada punto
    cursor.execute("""
        SELECT t.punto, t.fecha, t.valor
        FROM tblRegistro t
        INNER JOIN (
            SELECT punto, MAX(fecha) AS max_fecha
            FROM tblRegistro
            GROUP BY punto
        ) sub ON t.punto = sub.punto AND t.fecha = sub.max_fecha
        ORDER BY t.punto;
    """)

    # Convertir los datos a una lista de diccionarios
    datos = [
        {"punto": row[0], "fecha": row[1].strftime("%Y-%m-%d %H:%M:%S"), "valor": row[2]}
        for row in cursor.fetchall()
    ]

    # Cerrar conexión
    cursor.close()
    conn.close()

    return JsonResponse({"data": datos})