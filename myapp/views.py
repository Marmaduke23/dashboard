from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse  # Importa HttpResponse para enviar texto como respuesta
from django.http import JsonResponse
from .functions import cargar_datos, crear_boton
import json

@login_required 
def home(request):
    return render(request, 'home.html')  # Respuesta para la ruta '/'

def about(request):
    return HttpResponse("¡Esta es la página 'Acerca de'!")  # Respuesta para la ruta '/about'

from django.http import JsonResponse
import random

@login_required 
def dashboard(request):
    """Renderiza la página del dashboard."""
    return render(request, "dashboard.html")

# URL de descarga
onedrive_url = "https://immaipu-my.sharepoint.com/personal/karen_arancibia_maipu_cl/_layouts/15/download.aspx?share=Ec0mjRB4LrtCowyUYI11QVEBQ-XnXwoR48kodbA5qBUprg"

# Vista para actualizar el dashboard
def actualizar_dashboard(request):
    df = cargar_datos(onedrive_url)
    
    if df is not None:
        boton_1a = crear_boton(df, 'Pozo 1A - Funcionamiento', 'Sí', 'Pozo 1A - Caudal l/s')
        boton_2a = crear_boton(df, 'Pozo 2A - Funcionamiento', 'Sí', 'Pozo 2A - Caudal l/s')
        boton_3a = crear_boton(df, 'Pozo 3A - Funcionamiento', 'Sí', 'Pozo 3A - Caudal l/s')
        boton_4a = crear_boton(df, 'Pozo 4A - Funcionamiento', 'Sí', 'Pozo 4A - Caudal l/s')
        boton_5 = crear_boton(df, 'Pozo 5 - Funcionamiento', 'Sí', 'Pozo 5 - Caudal l/s')
        
        return JsonResponse({
            'botonPozo1A': boton_1a,
            'botonPozo2A': boton_2a,
            'botonPozo3A': boton_3a,
            'botonPozo4A': boton_4a,
            'botonPozo5': boton_5
        })
    else:
        return JsonResponse({'error': 'No se pudieron cargar los datos'}, status=500)