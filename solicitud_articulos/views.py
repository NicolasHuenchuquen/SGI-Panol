from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SolicitudArticuloForm
from .models import SolicitudArticulo
from gestor_inventario.models import Articulo

def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudArticuloForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)

            
            articulo = Articulo.objects.filter(cod_articulo=solicitud.cod_articulo).first()

            if articulo:
                if articulo.cantidad >= solicitud.cantidad:
                    articulo.cantidad -= solicitud.cantidad
                    articulo.save()
                    solicitud.save()
                    messages.success(request, 'La solicitud se ha creado correctamente y el stock se ha actualizado.')
                    return redirect('formulario_solicitudes') 
                elif articulo.cantidad < solicitud.cantidad:
                    messages.error(request, 'No hay stock suficiente para la solicitud')

            else:
                # Mensaje de error si el artículo no se encuentra
                messages.error(request, 'El artículo con el código proporcionado no existe.')
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, 'Por favor, corrija los errores en el formulario.')

    else:
        form = SolicitudArticuloForm()

    return render(request, 'solicitudes/formulario_solicitudes.html', {'form': form})

def historial_solicitudes(request):
    solicitudes = SolicitudArticulo.objects.all()
    solicitudes_con_nombre = []
    
    for solicitud in solicitudes:
        articulo = Articulo.objects.get(cod_articulo=solicitud.cod_articulo)
        solicitudes_con_nombre.append({
            'solicitud': solicitud,
            'nombre_articulo': articulo.nombre  
        })
    
    return render(request, 'solicitudes/historial_solicitudes.html', {'solicitudes_con_nombre': solicitudes_con_nombre})

def actualizar_estado_devolucion(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArticulo, id=solicitud_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_devolucion')
        

        if nuevo_estado:
            solicitud.estado_devolucion = nuevo_estado
            solicitud.save()
            messages.success(request, 'Estado de devolución actualizado exitosamente.')
        else:
            messages.error(request, 'Error al actualizar el estado de devolución.')

    return redirect('historial_solicitudes')