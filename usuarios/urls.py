from django.contrib import admin
from django.urls import path
from gestor_inventario import views
from usuarios import views
urlpatterns = [
    path('registrar-panolero/', views.registrar_panolero, name="registrar_panolero"),
]
