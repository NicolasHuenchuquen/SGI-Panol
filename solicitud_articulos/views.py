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

                cod_articulo = form.cleaned_data.get(cod_articulo_field)
                cantidad = form.cleaned_data.get(cantidad_field)

                if cod_articulo and cantidad:
                    cantidades_por_articulo[cod_articulo] += cantidad  # Acumular cantidad para este código

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

@login_required(login_url='sesion_cerrada')
def historial_solicitudes(request):
    query = request.GET.get('q', '').strip()
    fecha_salida_inicio = request.GET.get('fecha_salida_inicio', '')
    fecha_salida_fin = request.GET.get('fecha_salida_fin', '')
    fecha_devolucion_inicio = request.GET.get('fecha_devolucion_inicio', '')
    fecha_devolucion_fin = request.GET.get('fecha_devolucion_fin', '')
    estado_devolucion = request.GET.get('estado_devolucion', '')
    solicitudes = SolicitudArticulo.objects.all()
    articulos = Articulo.objects.all()

    # Recoger los valores de los 20 códigos de artículo y cantidades
    cod_articulos = [request.GET.get(f'cod_articulo{i}', '').strip() for i in range(1, 21)]
    cantidades = [request.GET.get(f'cantidad{i}', '').strip() for i in range(1, 21)]  # Nueva lógica para cantidad

    # Filtrar por nombre, rut o asignatura si existe el query
    if query:
        solicitudes = solicitudes.filter(
            Q(nombre_apellido__icontains=query) |
            Q(rut__icontains=query) |
            Q(asignatura__icontains=query) |
            Q(estado_devolucion__icontains=query)
        )

    # Filtrar por rango de fechas si existe
    if fecha_salida_inicio and fecha_salida_fin:
        solicitudes = solicitudes.filter(fecha_salida__range=[fecha_salida_inicio, fecha_salida_fin])

    if fecha_devolucion_inicio and fecha_devolucion_fin:
        solicitudes = solicitudes.filter(fecha_devolucion__range=[fecha_devolucion_inicio, fecha_devolucion_fin])

    # Filtrar por los códigos de artículo proporcionados
    for i, cod_articulo in enumerate(cod_articulos, 1):
        if cod_articulo:
            solicitudes = solicitudes.filter(**{f'cod_articulo{i}__icontains': cod_articulo})

    # Filtrar por las cantidades proporcionadas
    for i, cantidad in enumerate(cantidades, 1):
        if cantidad:
            solicitudes = solicitudes.filter(**{f'cantidad{i}__icontains': cantidad})
    
    if estado_devolucion:
        solicitudes = solicitudes.filter(estado_devolucion__iexact=estado_devolucion)

    # Hacer una consulta para obtener todos los artículos necesarios
    articulos_dict = {articulo.cod_articulo: articulo.nombre for articulo in Articulo.objects.filter(
        cod_articulo__in=[getattr(solicitud, f'cod_articulo{i}', None) for solicitud in solicitudes for i in range(1, 21) if getattr(solicitud, f'cod_articulo{i}', None)]
    )}

    solicitudes_con_nombre = []

    for solicitud in solicitudes:
        articulos_info = []
        nombres_articulos = []
        cantidades_info = []  # Para almacenar las cantidades

        # Recorremos los 20 artículos de cada solicitud
        for i in range(1, 21):
            cod_articulo = getattr(solicitud, f'cod_articulo{i}', None)
            cantidad = getattr(solicitud, f'cantidad{i}', None)
            if cod_articulo:
                # Usar el diccionario para obtener el nombre del artículo
                nombre_articulo = articulos_dict.get(cod_articulo, "Artículo no encontrado")
                nombres_articulos.append(nombre_articulo)
                articulos_info.append(cod_articulo)
            else:
                nombres_articulos.append(None)
                articulos_info.append(None)

            # Agregar la cantidad si existe
            if cantidad:
                cantidades_info.append(cantidad)
            else:
                cantidades_info.append(None)

        # Ahora combinamos los tres valores (código, nombre, cantidad) usando zip
        articulos_combinados = zip_longest(articulos_info, nombres_articulos, cantidades_info, fillvalue=None)

        # Añadimos los artículos combinados a la solicitud
        solicitudes_con_nombre.append({
            'solicitud': solicitud,
            'articulos_combinados': articulos_combinados,
        })

    # Contexto para el template
    context = {
        'solicitudes_con_nombre': solicitudes_con_nombre,
        'estado_devolucion': estado_devolucion,
    }

    return render(request, 'solicitudes/historial_solicitudes.html', context)

@login_required(login_url='sesion_cerrada')
def actualizar_estado_devolucion(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudArticulo, id=solicitud_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_devolucion')

        if nuevo_estado:
            # Verificar si el estado cambia a 'devuelto' y no estaba ya devuelto
            if nuevo_estado == 'devuelto' and solicitud.estado_devolucion != 'devuelto':
                errores = []

                # Procesar todos los artículos asociados a la solicitud
                for i in range(1, 21):
                    cod_articulo = getattr(solicitud, f'cod_articulo{i}', None)
                    cantidad = getattr(solicitud, f'cantidad{i}', None)

                    if cod_articulo and cantidad:  # Validar que el artículo y la cantidad existen
                        try:
                            articulo = Articulo.objects.get(cod_articulo=cod_articulo)
                            articulo.cantidad += cantidad
                            articulo.save()
                        except Articulo.DoesNotExist:
                            errores.append(f"El artículo con código {cod_articulo} no existe.")

                if errores:
                    # Si hubo errores, mostrarlos y no cambiar el estado de devolución
                    for error in errores:
                        messages.error(request, error)
                    return redirect('historial_solicitudes')

            # Actualizar el estado de devolución de la solicitud
            solicitud.estado_devolucion = nuevo_estado
            solicitud.save()
            messages.success(request, 'Estado de devolución actualizado exitosamente.')
        else:
            messages.error(request, 'Error al actualizar el estado de devolución.')

    return redirect('historial_solicitudes')