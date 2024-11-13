from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormArticuloInsumo, FormArticuloActivo
from sgipañol.views import navbar
from .models import Articulo
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def tabla_articulos(request):
    articulos = Articulo.objects.all()
    data = {'articulos' : articulos}
    return render(request, 'inventario/tabla_articulos.html', data)

@login_required
def agregar_insumo(request):
    form = FormArticuloInsumo()
    if request.method == 'POST':
        form = FormArticuloInsumo(request.POST)
        if form.is_valid():
            form.save()
            return navbar(request)
        data = {'form' : form}
    data = {'form' : form}
    return render(request, 'inventario/agregar_insumo.html', data)

@login_required
def agregar_activo(request):
    form = FormArticuloActivo()
    if request.method == 'POST':
        form = FormArticuloActivo(request.POST)
        if form.is_valid():
            form.save()
            return navbar(request)
        data = {'form' : form}
    data = {'form' : form}
    return render(request, 'inventario/agregar_activo.html', data)

@login_required
def editar_articulo(request):
    if request.method == 'POST':
        cod_articulo_tabla = request.POST.get('cod_articulo')
        tipo_articulo_tabla = request.POST.get('tipo_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_tabla)
        
        # Redirige a diferentes formularios según el tipo de artículo
        if tipo_articulo_tabla == 'Insumo':
            form = FormArticuloInsumo(instance=articulo)
            if form.is_valid():
                form.save()
                return tabla_articulos(request)
            data = {'form' : form} 
            
        elif tipo_articulo_tabla == 'Activo':
            form = FormArticuloActivo(instance=articulo)
            if form.is_valid():
                form.save()
                return tabla_articulos(request)
            data = {'form' : form} 
        else:
            return HttpResponseForbidden("Tipo de artículo no válido")
    return HttpResponseForbidden("Acceso no permitido")

@login_required
def eliminar_articulo(request):
    if request.method == 'POST':
        cod_articulo_form = request.POST.get('cod_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
        articulo.delete()
        return redirect('tabla_articulos') 
    return HttpResponseForbidden("Acceso no permitido")