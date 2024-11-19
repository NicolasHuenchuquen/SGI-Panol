from django.urls import path
from solicitud_articulos import views

urlpatterns = [
    path('formulario-solicitudes/', views.crear_solicitud, name='formulario_solicitudes'),
    path('historial-solicitudes/', views.historial_solicitudes, name='historial_solicitudes'),
    path('estado-devolucion/<int:solicitud_id>/', views.actualizar_estado_devolucion, name='actualizar_estado_devolucion'),
]