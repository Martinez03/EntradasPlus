from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import Empresa, Evento, Mensaje
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.db.models import Q  # Asegúrate de importar Q para las búsquedas
from django.utils import timezone  # Para manejar fechas con soporte de zona horaria
from .forms import EventoForm,EmpresaForm,RegisterForm, MensajeForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .decorators import empresa_verificada_required

def index(request):
    # Usamos timezone.now() para manejar fechas con zona horaria si es necesario
    entradas = models.Entrada.objects.filter(evento__fecha_evento__gte=timezone.now()).order_by('evento__fecha_evento')
    user_empresa = False
    if request.user.is_authenticated:
        try:
            user_empresa = Empresa.objects.filter(usuario=request.user).exists()
        except Empresa.DoesNotExist:
            user_empresa = False
    print(user_empresa)
    return render(request, 'index.html', {
        'entradas': entradas ,
        'user_empresa': user_empresa
    })

def calendar(request):
    return render(request, 'calendar.html', {})

def colaboradores(request):
    return render(request, 'colaboradores.html')

def miEmpresa(request):
    if request.user.is_authenticated:
        user_empresa = True
        empresa = Empresa.objects.get(usuario=request.user)    
    return render(request, 'mi_empresa.html', {
        'empresa': empresa ,
        'user_empresa': user_empresa
    })
   

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
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('/')  # Redirige a la página principal o la ruta deseada después de registrarse
        else:
            messages.error( request,'Hubo un error al crear el usuario, intentelo mas tarde.')
            return redirect('/')  
        
def contactar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()  # Esto creará la empresa y el usuario
            return redirect('empresa_pendiente')  # Redirigir a la página de confirmación
    else:
        form = EmpresaForm()
    
    return render(request, 'contactar_empresa.html', {'form': form})


def verificar_estado_empresa(user):
    try:
        empresa = Empresa.objects.get(usuario=user)
        if empresa.estado == 'pendiente':
            return False
        return True
    except Empresa.DoesNotExist:
        return True  # Si no es una empresa, no hay problema

def comprar(request, evento_id):
    # Obtén el evento por su ID, o muestra un 404 si no se encuentra
    evento = get_object_or_404(Evento, id=evento_id)
    entradas = evento.entradas.all()
    
    # Puedes agregar más lógica aquí si es necesario

    return render(request, 'comprar.html', {'evento': evento , 'entradas': entradas })


def empresa_pendiente(request):
    return render(request, 'empresa_pendiente.html')

def chat_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    mensajes = evento.mensajes.order_by('fecha_creacion')  # Mensajes ordenados cronológicamente

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.evento = evento
            mensaje.usuario = request.user
            mensaje.save()
            return redirect('chat_evento', evento_id=evento_id)  # Refresca la página después de enviar el mensaje
    else:
        form = MensajeForm()

    return render(request, 'chat_evento.html', {
        'evento': evento,
        'mensajes': mensajes,
        'form': form,
    })

@empresa_verificada_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)  # Manejar también archivos como la imagen
        if form.is_valid():
            evento = form.save(commit=False)
            evento.creador = request.user  # Asignar el creador del evento como el usuario actual
            evento.save()
            return redirect('mis_eventos')  # Redirigir al listado de eventos de la empresa
    else:
        form = EventoForm()
    
    return render(request, 'events/crear_evento.html', {'form': form})



 


