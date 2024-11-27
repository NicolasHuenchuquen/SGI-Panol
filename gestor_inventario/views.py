from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormArticuloInsumo, FormArticuloActivo, FormArticuloEditar
from sgipañol.views import navbar
from .models import Articulo
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='sesion_cerrada')
def tabla_articulos(request):
    articulos = Articulo.objects.filter(dado_de_baja=False)
    data = {'articulos' : articulos}
    return render(request, 'inventario/tabla_articulos.html', data)

@login_required(login_url='sesion_cerrada')
def tabla_insumos(request):
    articulos = Articulo.objects.filter(tipo_articulo="Insumo",dado_de_baja=False)
    data = {'articulos': articulos}
    return render(request, 'inventario/tabla_insumos.html', data)

@login_required(login_url='sesion_cerrada')
def tabla_activos(request):
    articulos = Articulo.objects.filter(tipo_articulo="Activo",dado_de_baja=False)
    data = {'articulos': articulos}
    return render(request, 'inventario/tabla_activos.html', data)



@login_required(login_url='sesion_cerrada')
def agregar_insumo(request):
    form = FormArticuloInsumo()
    if request.method == 'POST':
        form = FormArticuloInsumo(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El Insumo ha sido ingresado correctamente.', extra_tags='agregar_insumo')
            return redirect('agregar_insumo')  # Redirige a la misma página para que el mensaje se muestre
    data = {'form': form}
    return render(request, 'inventario/agregar_insumo.html', data)

@login_required(login_url='sesion_cerrada')
def agregar_activo(request):
    form = FormArticuloActivo()
    if request.method == 'POST':
        form = FormArticuloActivo(request.POST)
        if form.is_valid():
            
            form.save()
            messages.success(request, 'El Activo ha sido ingresado correctamente.', extra_tags='agregar_activo')
            return redirect('agregar_activo')
        else:
            print("Formulario no válido", form.errors)  # Mostrara los errores del formulario
    return render(request, 'inventario/agregar_activo.html', {'form': form})


@login_required(login_url='sesion_cerrada')
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
                messages.success(request, 'Artículo guardado correctamente.', extra_tags='articulo_editado')
                
                # Redirige según origen
                if tabla_origen == 'tabla_insumos':
                    return redirect('tabla_insumos')
                
                elif tabla_origen == 'tabla_activos':
                    return redirect('tabla_activos')
                
                elif tabla_origen == 'tabla_general':
                    return redirect('tabla_articulos')
                
                elif tabla_origen == 'General':
                    return redirect('tabla_bajas')
                
                elif tabla_origen == 'Insumo_baja':
                    return redirect('tabla_bajas_tipo', tipo='Insumo_baja')
                
                elif tabla_origen == 'Activo_baja':
                    return redirect('tabla_bajas_tipo', tipo='Activo_baja')
                
                return redirect('tabla_bajas')
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


@login_required(login_url='sesion_cerrada')
def dar_de_baja_articulo(request):
    cod_articulo_form = request.POST.get('cod_articulo')
    tabla_origen = request.POST.get('tabla_origen')
    
    articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
    articulo.dado_de_baja = True
    articulo.save()
    # Redirige según el origen
    if tabla_origen == 'tabla_insumos':
        return redirect('tabla_insumos')
    elif tabla_origen == 'tabla_activos':
        return redirect('tabla_activos')
    else:
        return redirect('tabla_articulos')
    


@login_required(login_url='sesion_cerrada')
def tabla_bajas(request, tipo=None):
    if tipo == "Insumo_baja":
        articulos = Articulo.objects.filter(dado_de_baja=True, tipo_articulo="Insumo")
    elif tipo == "Activo_baja":
        articulos = Articulo.objects.filter(dado_de_baja=True, tipo_articulo="Activo")
    else:  # General
        articulos = Articulo.objects.filter(dado_de_baja=True)
    
    data = {
        'articulos': articulos,
        'tipo_tabla': tipo if tipo else "General"
    }
    return render(request, 'inventario/tabla_bajas.html', data)


@login_required(login_url='sesion_cerrada')
def cancelar_baja(request):
    cod_articulo_form = request.POST.get('cod_articulo')
    tipo_tabla = request.POST.get('tipo_tabla')  # Puede ser "Insumo_baja", "Activo_baja" o "General" (valor predeterminado)

    # Recuperar y actualizar el estado del artículo
    articulo = get_object_or_404(Articulo, cod_articulo=cod_articulo_form)
    articulo.dado_de_baja = False
    articulo.save()
    

    # Redirigir según el origen de la tabla
    if tipo_tabla == 'Insumo_baja':
        return redirect('tabla_bajas_tipo', tipo='Insumo_baja')
    elif tipo_tabla == 'Activo_baja':
        return redirect('tabla_bajas_tipo', tipo='Activo_baja')
    else:  # General
        return redirect('tabla_bajas')


#CODIGO PARA ELIMINAR ARTICULOS DADOS DE BAJA SI EN ALGUN MOMENTO SE NECESITA
# @login_required(login_url='sesion_cerrada')
# def eliminar_articulo(request):
#     cod_articulo_form = request.POST.get('cod_articulo')
#     tipo_tabla = request.POST.get('tipo_tabla')  # Puede ser "Insumo", "Activo" o "General" (valor predeterminado)
#     articulo = Articulo.objects.get(cod_articulo = cod_articulo_form)
#     articulo.delete()

#     # Redirigir según el origen de la tabla
#     if tipo_tabla == 'Insumo':
#         return redirect('tabla_bajas_tipo', tipo='Insumo')
#     elif tipo_tabla == 'Activo':
#         return redirect('tabla_bajas_tipo', tipo='Activo')
#     else:  # General
#         return redirect('tabla_bajas')
