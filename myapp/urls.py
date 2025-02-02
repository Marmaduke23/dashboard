from django.urls import path, include  # Importa la función path para definir rutas
from . import views  # Importa las vistas de tu aplicación

urlpatterns = [
    path('', views.home, name='home'),  # Ruta principal (vacía, para la página inicial)
    path('about/', views.about, name='about'),  # Otra ruta, por ejemplo, "Acerca de"
    path('dashboard/', views.dashboard, name='dashboard'),  # Página con el gráfico
    path('api/actualizar_dashboard/', views.actualizar_dashboard, name='actualizar_dashboard'),  # API para los datos
   
]