from usuarios.forms import PanoleroCreationForm
from usuarios.models import Perfil
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

@login_required
def registrar_panolero(request):
    if not request.user.is_superuser: 
        raise PermissionDenied("No tienes permiso para crear usuarios pañoleros")
    
    if request.method == "POST":
        form = PanoleroCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pañolero agregado exitosamente.")
            return redirect('navbar')  # Redirige a la página deseada después de guardar
        else:
            # Si hay errores, se muestran todos al renderizar de nuevo el formulario
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PanoleroCreationForm()
    
    return render(request, 'usuarios/registrar_panolero.html', {'form': form})
