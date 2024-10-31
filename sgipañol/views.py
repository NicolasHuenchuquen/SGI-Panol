from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages


@login_required
def navbar(request):
    return render(request, 'navegacion/navbar.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Por favor ingrese tanto el nombre de usuario como la contraseña.')
        else:
            # Autenticación del usuario
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'navbar')  # Redirigir a la URL siguiente o 'navbar'
                return redirect(next_url)
            else:
                messages.error(request, 'Nombre de usuario o contraseña no válidos')
    
    return render(request, 'navegacion/iniciar_sesion.html')


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')