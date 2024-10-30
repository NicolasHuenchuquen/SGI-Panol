from django.shortcuts import render, redirect
from .forms import FormArticulo
from sgipañol.views import navbar
# Create your views here.

def agregar_insumo(request):
    form = FormArticulo()
    if request.method == 'POST':
        form = FormArticulo(request.POST)
        if form.is_valid():
            form.save()
            return navbar(request)
        data = {'form' : form}
    data = {'form' : form}
    return render(request, 'navegacion/agregar_insumo.html', data)

