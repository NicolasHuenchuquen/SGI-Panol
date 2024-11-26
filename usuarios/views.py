from usuarios.forms import PanoleroCreationForm
from usuarios.models import Perfil
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def sesion_cerrada(request):
    # Mostrar mensaje de que la sesión expiró o la sesión fue cerrada
    messages.error(request, 'Tu sesión ha expirado o no estás autenticado. Por favor, inicia sesión nuevamente.', extra_tags='sesion_cerrada')
    return redirect('iniciar_sesion')  # Redirige al login

@login_required(login_url='sesion_cerrada')
def registrar_panolero(request):
    if not request.user.is_superuser: 
        raise PermissionDenied("No tienes permiso para crear usuarios pañoleros")
    
    if request.method == "POST":
        form = PanoleroCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pañolero agregado exitosamente.", extra_tags='usuario_nuevo')
            return redirect('registrar_panolero')  # Redirige a la página deseada después de guardar
        else:
            # Si hay errores, se muestran todos al renderizar de nuevo el formulario
            messages.error(request, "Por favor corrige los errores en el formulario.",extra_tags='aviso_form')
    else:
        form = PanoleroCreationForm()
    
    return render(request, 'usuarios/registrar_panolero.html', {'form': form})
