from django.urls import path
from solicitud_articulos import views

urlpatterns = [
    path('formulario-solicitudes/', views.crear_solicitud, name='formulario_solicitudes'),
]