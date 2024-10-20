from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import Empresa, Evento
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.db.models import Q  # Asegúrate de importar Q para las búsquedas
from django.utils import timezone  # Para manejar fechas con soporte de zona horaria
from .forms import EventoForm,EmpresaForm

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




def login_empresa(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            # Buscar la empresa por su correo electrónico
            empresa = Empresa.objects.get(email=email)
            
            # Verificar la contraseña
            if check_password(password, empresa.password):
                # Crear la sesión para la empresa
                request.session['empresa_id'] = empresa.id
                messages.success(request, f'Bienvenido, {empresa.nombre}!')
                return redirect('home')  # Redirigir a la página principal o al panel de la empresa
            else:
                messages.error(request, 'Contraseña incorrecta.')
                return redirect('login_empresa')
        except Empresa.DoesNotExist:
            messages.error(request, 'No se encontró una empresa con ese correo electrónico.')
            return redirect('login_empresa')

    
    return render(request, 'login_empresa.html')

def logout_empresa(request):

    # Eliminar la sesión de empresa
    if 'empresa_id' in request.session:
        del request.session['empresa_id']
        messages.success(request, 'Has cerrado sesión como empresa.')
    
    return redirect('home')  # Redirigir a la página principal

def registro_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            empresa = form.save(commit=False)
            empresa.password = make_password(form.cleaned_data['password'])  # Encriptar la contraseña
            empresa.save()
            messages.success(request, 'Empresa registrada con éxito.')
            return redirect('login_empresa')
    else:
        form = EmpresaForm()

    return render(request, 'registro_empresa.html', {'form': form})

def trending(request):
    eventos = Evento.objects.all()
    context = {
        'eventos': eventos, 
    }

    return render(request, 'trending.html', context)