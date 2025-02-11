from django.urls import path, include  # Importa la función path para definir rutas
from . import views  # Importa las vistas de tu aplicación
from .pr18chuchunco import *

urlpatterns = [
    path('', views.home, name='home'),  # Ruta principal (vacía, para la página inicial)
    path('about/', views.about, name='about'),  # Otra ruta, por ejemplo, "Acerca de"
    path('dashboard/', views.dashboard, name='dashboard'),  # Página con el gráfico
    path('api/actualizar_dashboard/', views.actualizar_dashboard, name='actualizar_dashboard'),
    path('datos/', views.obtener_datos, name='obtener_datos'),  # API para los datos de pcp
    path('historicos/', views.historicos, name='historicos'),  # Página con el gráfico
    path('reportes/', views.reportes, name='reportes'),  # Página con reportes
    path('generar_pr18/', views.generar_pr18, name='generar_pr18'),  # Página con reportes
   
]