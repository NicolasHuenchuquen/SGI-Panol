from django.contrib import admin
from django.urls import path
from gestor_inventario import views
from usuarios import views
urlpatterns = [
    path('registrar-panolero/', views.registrar_panolero, name="registrar_panolero"),
    path('sesion-cerrada/', views.sesion_cerrada, name='sesion_cerrada'),
]
