from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SolicitudArticuloForm

def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudArticuloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Solicitud enviada con éxito.")
            return redirect('formulario_solicitudes') 
        else:
            messages.error(request, "Hay errores en el formulario. Verifica los campos.")
    else:
        form = SolicitudArticuloForm()
    
    return render(request, 'solicitudes/formulario_solicitudes.html', {'form': form})
