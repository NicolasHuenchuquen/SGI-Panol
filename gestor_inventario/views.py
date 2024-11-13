from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormArticuloInsumo, FormArticuloActivo, FormArticuloEditar
from sgipañol.views import navbar
from .models import Articulo
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            
            form.save()
            return redirect('tabla_articulos')
        else:
            print("Formulario no válido", form.errors)  # Mostrara los errores del formulario
    return render(request, 'inventario/agregar_activo.html', {'form': form})


@login_required
def editar_articulo(request):
    # Obtiene el código del artículo del form del boton editar
    cod_articulo = request.POST.get('cod_articulo') or request.GET.get('cod_articulo')
    
    if not cod_articulo:
        messages.error(request, 'No se proporcionó código de artículo')
        return redirect('tabla_articulos')
    
    # Obtiene el artículo que coincida con el codigo del objeto a editar con uno de la base de datos
    articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo)
    
    if request.method == 'POST':
        form = FormArticuloEditar(request.POST, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Artículo actualizado correctamente')
            return redirect('tabla_articulos')
    else:
        # Para peticiones GET, inicializar el formulario con la instancia del artículo
        form = FormArticuloEditar(instance=articulo)
    
    data = {
        'form': form,
        'articulo': articulo,
    }
    
    return render(request, 'inventario/editar_articulo.html', data)


@login_required
def eliminar_articulo(request):
    if request.method == 'POST':
        cod_articulo_form = request.POST.get('cod_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
        articulo.delete()
        return redirect('tabla_articulos') 
    return HttpResponseForbidden("Acceso no permitido")