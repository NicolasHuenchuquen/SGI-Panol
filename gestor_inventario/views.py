from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormArticuloInsumo, FormArticuloActivo, FormArticuloEditar
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
            return redirect('tabla_articulos')
        data = {'form' : form}
    data = {'form' : form}
    return render(request, 'inventario/agregar_insumo.html', data)

@login_required
def agregar_activo(request):
    form = FormArticuloActivo()
    if request.method == 'POST':
        form = FormArticuloActivo(request.POST)
        if form.is_valid():
            print("Formulario válido")  # Verifica si está pasando por aquí
            form.save()
            return redirect('tabla_articulos')
        else:
            print("Formulario no válido", form.errors)  # Imprime los errores del formulario
    return render(request, 'inventario/agregar_activo.html', {'form': form})


@login_required
def editar_articulo(request):
    if request.method == 'POST':
        cod_articulo_tabla = request.POST.get('cod_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_tabla)
        
        # Carga el formulario con los datos enviados para editar el artículo
        form = FormArticuloEditar(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            return redirect('tabla_articulos')  # Redirige a la vista de la tabla de artículos

    else:
        # Si es una solicitud GET, carga el formulario con la instancia del artículo
        cod_articulo_tabla = request.GET.get('cod_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_tabla)
        form = FormArticuloEditar(instance=articulo)

    # Pasa el formulario a la plantilla para su renderizado
    data = {'form': form}
    return render(request, 'inventario/editar_articulo.html', data)



@login_required
def eliminar_articulo(request):
    if request.method == 'POST':
        cod_articulo_form = request.POST.get('cod_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
        articulo.delete()
        return redirect('tabla_articulos') 
    return HttpResponseForbidden("Acceso no permitido")