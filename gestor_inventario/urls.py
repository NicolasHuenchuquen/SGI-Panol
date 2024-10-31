from django.contrib import admin
from django.urls import path
from gestor_inventario import views
urlpatterns = [
    path('agregar_insumo/', views.agregar_insumo, name="agregar_insumo"),
]
