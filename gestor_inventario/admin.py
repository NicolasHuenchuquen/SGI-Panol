from django.contrib import admin
from usuarios.models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo_usuario', 'rut')
    search_fields = ('user__username', 'rut')
    list_filter = ('tipo_usuario',)  

admin.site.register(Perfil, PerfilAdmin)