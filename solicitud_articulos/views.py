from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SolicitudArticuloForm
from .models import SolicitudArticulo
from gestor_inventario.models import Articulo
from django.db.models import Q
from datetime import datetime

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
                    messages.success(request, 'La solicitud se ha creado correctamente y el stock se ha actualizado.', extra_tags='solicitud_creada')
                    return redirect('formulario_solicitudes') 
                elif articulo.cantidad < solicitud.cantidad:
                    messages.error(request, 'No hay stock suficiente para la solicitud', extra_tags='avisos_form')

            else:
                # Mensaje de error si el artículo no se encuentra
                messages.error(request, 'El artículo con el código proporcionado no existe.', extra_tags='avisos_form')
        else:
            # Mensaje de error si el formulario no es válido
            messages.error(request, 'Por favor, corrija los errores en el formulario.', extra_tags='avisos_form')

    else:
        form = SolicitudArticuloForm()

    return render(request, 'solicitudes/formulario_solicitudes.html', {'form': form})

def historial_solicitudes(request):
    query = request.GET.get('q', '').strip()  # Captura el término de búsqueda
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    solicitudes = SolicitudArticulo.objects.all()

    if query:
        solicitudes = solicitudes.filter(
            Q(nombre_apellido__icontains=query) |
            Q(rut__icontains=query) |
            Q(asignatura__icontains=query)
        )

    if fecha_inicio and fecha_fin:
        solicitudes = solicitudes.filter(fecha_salida__range=[fecha_inicio, fecha_fin])

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
            # Verificar si el estado cambia a 'devuelto' y no estaba ya devuelto
            if nuevo_estado == 'devuelto' and solicitud.estado_devolucion != 'devuelto':
                try:
                    articulo = Articulo.objects.get(cod_articulo=solicitud.cod_articulo)
                    
                    articulo.cantidad += solicitud.cantidad
                    articulo.save()
                except Articulo.DoesNotExist:
                    messages.error(request, 'El artículo asociado a esta solicitud no existe.')
                    return redirect('historial_solicitudes')

            solicitud.estado_devolucion = nuevo_estado
            solicitud.save()
            messages.success(request, 'Estado de devolución actualizado exitosamente.')
        else:
            messages.error(request, 'Error al actualizar el estado de devolución.')

    return redirect('historial_solicitudes')