from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SolicitudArticuloForm
from .models import SolicitudArticulo
from gestor_inventario.models import Articulo
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.views.generic.edit import FormView
from itertools import zip_longest
from collections import defaultdict
from django.utils import timezone

@login_required(login_url='sesion_cerrada')
def crear_solicitud(request):
    if request.method == 'POST':
        form = SolicitudArticuloForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)  # Guardar sin comprometer datos aún
            errores_stock = []
            articulos_actualizados = []
            cantidades_por_articulo = defaultdict(int)  # Para acumular cantidades por código de artículo

            # Procesar dinámicamente los artículos solicitados
            for i in range(1, 21):
                cod_articulo_field = f'cod_articulo{i}'
                cantidad_field = f'cantidad{i}'

                # Obtener los valores de los campos dinámicos
                cod_articulo = form.cleaned_data.get(cod_articulo_field)
                cantidad = form.cleaned_data.get(cantidad_field, 0)

                if cod_articulo:  # Solo procesar si hay un valor válido
                    cod_articulo = cod_articulo.strip().upper()

                    # Almacenar el código de artículo transformado
                    form.cleaned_data[cod_articulo_field] = cod_articulo  # Reasignar el valor transformado

                    # Acumular cantidad para este código
                    cantidades_por_articulo[cod_articulo] += cantidad

            # Validar stock y actualizar artículos
            for cod_articulo, total_cantidad in cantidades_por_articulo.items():
                articulo = Articulo.objects.filter(cod_articulo=cod_articulo, dado_de_baja=False).first()

                if articulo:
                    if articulo.cantidad >= total_cantidad:
                        articulo.cantidad -= total_cantidad
                        articulos_actualizados.append(articulo)
                    else:
                        errores_stock.append(
                            f"No hay stock suficiente para el artículo {cod_articulo}. Disponible: {articulo.cantidad}, solicitado: {total_cantidad}."
                        )
                else:
                    if Articulo.objects.filter(cod_articulo=cod_articulo).exists():
                        errores_stock.append(f"El artículo {cod_articulo} está dado de baja.")
                    else:
                        errores_stock.append(f"El artículo {cod_articulo} no existe.")

            if errores_stock:
                for error in errores_stock:
                    messages.error(request, error, extra_tags='avisos_form')
            else:
                for articulo in articulos_actualizados:
                    articulo.save()
                solicitud.save()
                messages.success(request, 'La solicitud se ha creado correctamente y el stock se ha actualizado.', extra_tags='solicitud_creada')
                return redirect('formulario_solicitudes')
        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.', extra_tags='avisos_form')
    else:
        form = SolicitudArticuloForm()

    return render(request, 'solicitudes/formulario_solicitudes.html', {'form': form})

from django.utils import timezone


@login_required(login_url='sesion_cerrada')
def historial_solicitudes(request):
    # Obtener la fecha y hora actuales
    now = timezone.now()

    # Actualizar automáticamente los registros atrasados
    atrasados_actualizados = SolicitudArticulo.objects.filter(
        estado_devolucion='no devuelto',
    ).filter(
        # Verificar si la fecha de devolución es menor a la actual
        Q(fecha_devolucion__lt=now.date()) | 
        # O si la fecha de devolución es hoy y la hora ya pasó
        Q(fecha_devolucion=now.date(), hora_devolucion__lt=now.time())
    ).update(atrasado=True)

    print(f"Atrasados actualizados: {atrasados_actualizados}")  # Log para depuración

    # Actualizar solicitudes con estado de devolución devuelto o parcialmente devuelto
    solicitudes_actualizadas = SolicitudArticulo.objects.filter(
        estado_devolucion__in=['devuelto', 'parcialmente devuelto']
    ).update(atrasado=False)  # Actualizar 'atrasado' a False si ya fue devuelto

    print(f"Atrasados actualizados por devolución: {solicitudes_actualizadas}")  # Log para depuración

    # Filtros de búsqueda
    query = request.GET.get('q', '').strip()
    fecha_salida_inicio = request.GET.get('fecha_salida_inicio', '')
    fecha_salida_fin = request.GET.get('fecha_salida_fin', '')
    fecha_devolucion_inicio = request.GET.get('fecha_devolucion_inicio', '')
    fecha_devolucion_fin = request.GET.get('fecha_devolucion_fin', '')
    estado_devolucion = request.GET.get('estado_devolucion', '')
    atrasado = request.GET.get('atrasado', '')  # Filtro para "atrasado"

    # Base de solicitudes
    solicitudes = SolicitudArticulo.objects.all()

    # Filtro de búsqueda general
    if query:
        solicitudes = solicitudes.filter(
            Q(nombre_apellido__icontains=query) |
            Q(rut__icontains=query) |
            Q(asignatura__icontains=query) |
            Q(estado_devolucion__icontains=query)
        )

    # Filtro por rango de fechas de salida
    if fecha_salida_inicio and fecha_salida_fin:
        solicitudes = solicitudes.filter(fecha_salida__range=[fecha_salida_inicio, fecha_salida_fin])

    # Filtro por rango de fechas de devolución
    if fecha_devolucion_inicio and fecha_devolucion_fin:
        solicitudes = solicitudes.filter(fecha_devolucion__range=[fecha_devolucion_inicio, fecha_devolucion_fin])

    # Filtro por estado de devolución
    if estado_devolucion:
        solicitudes = solicitudes.filter(estado_devolucion__iexact=estado_devolucion)

    # Filtro por estado de "atrasado"
    if atrasado:
        if atrasado == 'True':
            solicitudes = solicitudes.filter(atrasado=True)
        elif atrasado == 'False':
            solicitudes = solicitudes.filter(atrasado=False)

    # Construir lista con nombres de artículos
    articulos_dict = {
        articulo.cod_articulo: articulo.nombre
        for articulo in Articulo.objects.filter(
            cod_articulo__in=[getattr(solicitud, f'cod_articulo{i}', None) for solicitud in solicitudes for i in range(1, 21) if getattr(solicitud, f'cod_articulo{i}', None)]
        )
    }

    # Asegurarnos de que todas las solicitudes tengan un encargado asignado
    if request.user.is_authenticated:
        for solicitud in solicitudes:
            if not solicitud.encargado:  # Si no tiene encargado
                solicitud.encargado = f"{request.user.first_name} {request.user.last_name}".strip()
                solicitud.save()

    # Hacer una consulta para obtener todos los artículos necesarios
    articulos_dict = {
    articulo.cod_articulo: {'nombre': articulo.nombre, 'tipo': articulo.tipo_articulo}
    for articulo in Articulo.objects.filter(
        cod_articulo__in=[getattr(solicitud, f'cod_articulo{i}', None) for solicitud in solicitudes for i in range(1, 21) if getattr(solicitud, f'cod_articulo{i}', None)]
    )
    }

    solicitudes_con_nombre = []

    for solicitud in solicitudes:
        articulos_info = []
        nombres_articulos = []
        tipos_articulos = []
        cantidades_info = []

        for i in range(1, 21):
            cod_articulo = getattr(solicitud, f'cod_articulo{i}', None)
            cantidad = getattr(solicitud, f'cantidad{i}', None)
            if cod_articulo:
                articulo_data = articulos_dict.get(cod_articulo, {"nombre": "Artículo no encontrado", "tipo": "Desconocido"})
                nombre_articulo = articulo_data["nombre"]
                tipo_articulo = articulo_data["tipo"]
                nombres_articulos.append(nombre_articulo)
                tipos_articulos.append(tipo_articulo)
                articulos_info.append(cod_articulo)
            else:
                nombres_articulos.append(None)
                tipos_articulos.append(None)
                articulos_info.append(None)

            if cantidad:
                cantidades_info.append(cantidad)
            else:
                cantidades_info.append(None)

        articulos_combinados = zip_longest(articulos_info, nombres_articulos, tipos_articulos, cantidades_info, fillvalue=None)

        solicitudes_con_nombre.append({
            'solicitud': solicitud,
            'articulos_combinados': articulos_combinados,
        })

    # Contexto para el template
    context = {
        'solicitudes_con_nombre': solicitudes_con_nombre,
        'estado_devolucion': estado_devolucion,
        'atrasado': atrasado,  # Añadimos el filtro "atrasado"
    }

    return render(request, 'solicitudes/historial_solicitudes.html', context)

@login_required(login_url='sesion_cerrada')
def actualizar_estado_devolucion(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArticulo, id=solicitud_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_devolucion')

        if nuevo_estado:
            # Si el estado es devuelto o parcialmente devuelto, actualizar el campo 'atrasado' a False
            if nuevo_estado in ['devuelto', 'parcialmente devuelto']:
                solicitud.atrasado = False  # El artículo ya fue devuelto, no está atrasado

            # Actualizamos el estado de devolución
            solicitud.estado_devolucion = nuevo_estado
            solicitud.save()  # Guardamos la solicitud con el nuevo estado

            # Actualizamos la cantidad de los artículos
            for i in range(1, 21):
                cod_articulo = getattr(solicitud, f'cod_articulo{i}', None)
                cantidad = getattr(solicitud, f'cantidad{i}', None)

                if cod_articulo and cantidad:  # Validar que el artículo y la cantidad existen
                    try:
                        articulo = Articulo.objects.get(cod_articulo=cod_articulo)
                        articulo.cantidad += cantidad
                        articulo.save()
                    except Articulo.DoesNotExist:
                        messages.error(request, f"El artículo con código {cod_articulo} no existe.")
                        return redirect('historial_solicitudes')

            messages.success(request, 'Estado de devolución actualizado exitosamente.')
        else:
            messages.error(request, 'Error al actualizar el estado de devolución.')

    return redirect('historial_solicitudes')
