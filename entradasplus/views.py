from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import Empresa, Evento
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.db.models import Q  # Asegúrate de importar Q para las búsquedas
from django.utils import timezone  # Para manejar fechas con soporte de zona horaria
from .forms import EventoForm,EmpresaForm,RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def index(request):
    # Usamos timezone.now() para manejar fechas con zona horaria si es necesario
    entradas = models.Entrada.objects.filter(evento__fecha_evento__gte=timezone.now()).order_by('evento__fecha_evento')
    return render(request, 'index.html', {
        'entradas': entradas 
    })

def calendar(request):
    return render(request, 'calendar.html', {})

def buscar_eventos(request):
    query = request.GET.get('q', '')
    if query:
        eventos = models.Evento.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(lugar__icontains=query)
        )
    else:
        eventos = models.Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Intentar autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si la autenticación es correcta, iniciar sesión
            login(request, user)
            return redirect('home')  # Redirigir al usuario después de iniciar sesión
        else:
            # Si la autenticación falla, mostrar un mensaje de error
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return redirect('home')  # Redirigir a la página de login si falla
    else:
        return render(request, 'index.html')

def detalles_evento(request, evento_id):
    # Importamos el modelo Evento si no está importado
    evento = get_object_or_404(models.Evento, pk=evento_id)  # Usa models.Evento
    return render(request, 'detalles_evento.html', {'evento': evento})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirige a la página principal después de cerrar sesión

def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.empresa = request.user.empresa  # Asignar la empresa organizadora
            evento.save()
            return redirect('home')  # Redirigir tras crear el evento
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form})

def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, empresa=request.user.empresa)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'editar_evento.html', {'form': form, 'evento': evento})

def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id, empresa=request.user.empresa)
    if request.method == 'POST':
        evento.delete()
        return redirect('home')
    return render(request, 'eliminar_evento.html', {'evento': evento})



def trending(request):
    eventos = Evento.objects.all()
    context = {
        'eventos': eventos, 
    }

    return render(request, 'trending.html', context)

def login_empresa(request):
    

    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirige a la página principal o la ruta deseada después de registrarse
        else:
            messages.error( request,'Hubo un error al crear el usuario, intentelo mas tarde.')
            return redirect('/')  
        
   
 


