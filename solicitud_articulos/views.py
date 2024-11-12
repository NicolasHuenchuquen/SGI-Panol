from django.shortcuts import render, redirect
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
    return render(request, 'solicitudes/historial_solicitudes.html', {'solicitudes': solicitudes})