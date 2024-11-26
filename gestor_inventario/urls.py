from django.contrib import admin
from django.urls import path
from gestor_inventario import views
urlpatterns = [
    path('agregar_insumo/', views.agregar_insumo, name="agregar_insumo"),
    path('agregar_activo/', views.agregar_activo, name="agregar_activo"),
    path('editar_articulo/',views.editar_articulo, name='editar_articulo'),
    path('baja_articulo/', views.dar_de_baja_articulo, name='baja_articulo'),

    path('cancelar_baja/', views.cancelar_baja, name='cancelar_baja'),

    path('inventario/', views.tabla_articulos, name='tabla_articulos'),
    path('inventario_insumos/', views.tabla_insumos, name='tabla_insumos'),
    path('inventario_activos/', views.tabla_activos, name='tabla_activos'),

    path('inventario_bajas/', views.tabla_bajas, name='tabla_bajas'),
    path('inventario_bajas/<str:tipo>/', views.tabla_bajas, name='tabla_bajas_tipo'),
    # path('eliminar_articulo/', views.eliminar_articulo, name='eliminar_articulo'),
]
