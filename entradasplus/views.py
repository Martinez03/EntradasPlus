from django.shortcuts import render
from . import models

def index(request):
    entradas = models.Entrada
    return render(request, 'index.html', {
        'entradas': entradas 
    })


def calendar(request):
    return render(request, 'calendar.html', {
    })
