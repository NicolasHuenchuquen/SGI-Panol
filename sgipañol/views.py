from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
#PARA MANEJAR EL ERROR DE CSRF TOKEN
from django.shortcuts import render



@login_required(login_url='sesion_cerrada')
def navbar(request):
    """
    Vista que renderiza la barra de navegación solo para usuarios autenticados.
    
    Esta vista requiere que el usuario esté autenticado. Si no lo está, lo redirige a la página de 
    inicio de sesión, indicada en `login_url='sesion_cerrada'`.

    Parameters:
    - request: El objeto de solicitud HTTP.

    Returns:
    - render: Renderiza la plantilla 'navegacion/nav.html' que muestra la barra de navegación.
    """
    return render(request, 'navegacion/nav.html')

def iniciar_sesion(request):
    """
    Vista para iniciar sesión en el sistema.

    Permite a los usuarios autenticarse mediante su nombre de usuario y contraseña. Si los datos son correctos,
    el usuario será autenticado y redirigido a la página que intentaba acceder o, si no se especificó una página,
    al formulario de solicitudes.

    Si las credenciales no son válidas, se muestra un mensaje de error al usuario.

    Parameters:
    - request: El objeto de solicitud HTTP.

    Returns:
    - render: Renderiza la plantilla 'navegacion/iniciar_sesion.html' para mostrar el formulario de inicio de sesión.
    - redirect: Si la autenticación es exitosa, redirige al usuario a la URL indicada.
    """
    if request.method == 'POST':
        # Obtiene el nombre de usuario y la contraseña desde el formulario de inicio de sesión
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica si ambos campos han sido llenados
        if not username or not password:
            # Si faltan datos, muestra un mensaje de error
            messages.error(request, 'Por favor ingrese tanto el nombre de usuario como la contraseña.', extra_tags='login_error')
        else:
            # Autentica al usuario con las credenciales proporcionadas
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Si la autenticación es exitosa, inicia sesión y redirige
                login(request, user)
                # Obtiene la URL a la que se debe redirigir (si existe en la petición GET, sino redirige a 'formulario_solicitudes')
                next_url = request.GET.get('next', 'formulario_solicitudes')
                return redirect(next_url)
            else:
                # Si las credenciales no son válidas, muestra un mensaje de error
                messages.error(request, 'Nombre de usuario o contraseña no válidos', extra_tags='login_error')

    # Renderiza el formulario de inicio de sesión
    return render(request, 'navegacion/iniciar_sesion.html')

@login_required(login_url='sesion_cerrada')
def cerrar_sesion(request):
    """
    Vista para cerrar sesión del usuario autenticado.

    Cuando el usuario cierra sesión, la sesión se destruye y se redirige al formulario de inicio de sesión.

    Parameters:
    - request: El objeto de solicitud HTTP.

    Returns:
    - redirect: Redirige al usuario a la página de inicio de sesión ('iniciar_sesion').
    """
    # Cierra la sesión del usuario
    logout(request)
    # Redirige al formulario de inicio de sesión
    return redirect('iniciar_sesion')



def csrf_error(request, reason=""):
    """
    Maneja los errores de CSRF (Cross-Site Request Forgery) y presenta una página de error adecuada.

    Cuando un error CSRF ocurre, esta función es llamada para informar al usuario sobre el error y permitir
    que puedan regresar a la página de origen desde donde intentaron realizar una acción no válida debido a CSRF.
    
    Parameters:
    - request: El objeto de solicitud HTTP.
    - reason: El motivo del error (por defecto está vacío, pero puede ser útil para dar más detalles sobre la causa).

    Returns:
    - render: Retorna una respuesta HTTP con el renderizado de la página de error CSRF.
    """

    # Obtiene la URL desde la que el usuario intentaba hacer la solicitud (HTTP_REFERER) para poder redirigirlo
    # de vuelta a esa página después del error, o al inicio si no se encuentra dicha información.
    referer = request.META.get('HTTP_REFERER', '/')

    # Renderiza la página de error CSRF, pasando un indicador de error y la razón del error si es proporcionada.
    return render(request, 'navegacion/csrf_error.html', {
        'error_csrf': True,   # Indicador de que hubo un error CSRF
        'reason': reason,      # Motivo del error (opcional, dependiendo de la causa específica)
        'referer': referer,    # La URL de la que el usuario provino, para redirigirlo o devolverlo a esa página.
    })

