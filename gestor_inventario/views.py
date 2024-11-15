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
    articulos = Articulo.objects.filter(dado_de_baja=False)
    data = {'articulos' : articulos}
    return render(request, 'inventario/tabla_articulos.html', data)

@login_required
def tabla_insumos(request):
    articulos = Articulo.objects.filter(tipo_articulo="Insumo",dado_de_baja=False)
    data = {'articulos': articulos}
    return render(request, 'inventario/tabla_insumos.html', data)

@login_required
def tabla_activos(request):
    articulos = Articulo.objects.filter(tipo_articulo="Activo",dado_de_baja=False)
    data = {'articulos': articulos}
    return render(request, 'inventario/tabla_activos.html', data)

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
    if request.method == 'POST':
        # Obtiene el código del artículo del form
        cod_articulo = request.POST.get('cod_articulo')
        tabla_origen = request.POST.get('tabla_origen')
        
        if not cod_articulo:
            messages.error(request, 'No se proporcionó código de artículo')
            return redirect('tabla_articulos')
        
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo)
        
        # Si viene el formulario completo (con los campos del artículo)
        if 'nombre' in request.POST:  # o cualquier campo de tu formulario
            form = FormArticuloEditar(request.POST, instance=articulo)
            if form.is_valid():
                form.save()
                messages.success(request, 'Artículo actualizado correctamente')
                
                # Redirige según origen
                if tabla_origen == 'tabla_insumos':
                    return redirect('tabla_insumos')
                elif tabla_origen == 'tabla_activos':
                    return redirect('tabla_activos')
                return redirect('tabla_articulos')
        else:
            # Si solo viene el código, muestra el formulario
            form = FormArticuloEditar(instance=articulo)
        
        data = {
            'form': form,
            'articulo': articulo,
            'tabla_origen': tabla_origen,
        }
        
        return render(request, 'inventario/editar_articulo.html', data)
    
    # Si alguien intenta acceder por GET, redirigir
    return redirect('tabla_articulos')


@login_required
def eliminar_articulo(request):
    if request.method == 'POST':
        cod_articulo_form = request.POST.get('cod_articulo')
        articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
        articulo.delete()
        return redirect('tabla_articulos') 
    return HttpResponseForbidden("Acceso no permitido")

@login_required
def dar_de_baja_articulo(request):
    cod_articulo_form = request.POST.get('cod_articulo')
    tabla_origen = request.POST.get('tabla_origen')
    
    articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
    articulo.dado_de_baja = True
    articulo.save()
    messages.success(request, 'Artículo marcado como dado de baja.')
    
    # Redirige según el origen
    if tabla_origen == 'tabla_insumos':
        return redirect('tabla_insumos')
    elif tabla_origen == 'tabla_activos':
        return redirect('tabla_activos')
    else:
        return redirect('tabla_articulos')
    