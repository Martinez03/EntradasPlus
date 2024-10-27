from django.shortcuts import render, redirect, get_object_or_404
from . import models
from .models import Empresa, Evento, Mensaje,Entrada
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.db.models import Q  # Asegúrate de importar Q para las búsquedas
from django.utils import timezone  # Para manejar fechas con soporte de zona horaria
from .forms import EventoForm,EmpresaForm,RegisterForm, MensajeForm, PerfilForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .decorators import empresa_verificada_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Grupo, SolicitudGrupo, MensajeGrupo
from .forms import GrupoForm, MensajeGrupoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Pedido, Grupo, PerfilUsuario

@login_required
def crear_grupo(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST, request.FILES)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.admin = request.user
            grupo.save()
            grupo.usuarios.add(request.user)  # El admin se une automáticamente
            return redirect('grupos')
    else:
        form = GrupoForm()
    return render(request, 'crear_grupo.html', {'form': form})

def lista_grupos(request):
    grupos = Grupo.objects.all()
    query = request.GET.get('q')
    if query:
        grupos = grupos.filter(nombre__icontains=query)
    return render(request, 'lista_grupos.html', {'grupos': grupos})

def detalles_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    mensajes = grupo.mensajes.all().order_by('fecha_creacion')
    form = MensajeGrupoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mensaje = form.save(commit=False)
        mensaje.grupo = grupo
        mensaje.usuario = request.user
        mensaje.save()
        return redirect('detalles_grupo', grupo_id=grupo.id)
    return render(request, 'detalles_grupo.html', {'grupo': grupo, 'mensajes': mensajes, 'form': form})


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


def logout_view(request):
    logout(request)
    return redirect('home')  # Redirige a la página principal después de cerrar sesión

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
            messages.error( request,'La contraseña debe contener caracteres y numeros')
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

def comprar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    perfil_usuario = PerfilUsuario.objects.get(user=request.user)

    if request.method == 'POST':
        entrada_id = request.POST.get('entrada_id')
        cantidad = int(request.POST.get('cantidad', 1))
        entrada = get_object_or_404(Entrada, id=entrada_id)

        total = cantidad * entrada.precio

        # Verificar disponibilidad de entradas y saldo del usuario
        if cantidad > entrada.cantidad_disponible:
            messages.error(request, f'Solo quedan {entrada.cantidad_disponible} entradas disponibles.')
            return redirect('comprar', evento_id=evento.id)

        if perfil_usuario.dinero < total:
            messages.error(request, f'No tienes suficiente dinero. Te faltan {total - perfil_usuario.dinero}€.')
            return redirect('comprar', evento_id=evento.id)

        # Actualizar inventario y saldo del usuario
        entrada.cantidad_disponible -= cantidad
        perfil_usuario.dinero -= total
        entrada.save()
        perfil_usuario.save()

        # Registrar el pedido
        Pedido.objects.create(
            usuario=request.user,
            entrada=entrada,
            cantidad=cantidad,
            fecha_compra=timezone.now(),
            total=total
        )

        messages.success(request, '¡Compra realizada con éxito!')
        return redirect('home')

    return redirect('comprar', evento_id=evento.id)
    
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

@login_required
def crear_grupo(request):
    # Limitar a 3 grupos por usuario
    if Grupo.objects.filter(admin=request.user).count() >= 3:
        messages.warning(request, 'Has alcanzado el límite de 3 grupos. Para crear uno nuevo, debes eliminar alguno existente.')
        return redirect('lista_grupos')

    if request.method == 'POST':
        form = GrupoForm(request.POST, request.FILES)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.admin = request.user
            grupo.save()
            grupo.usuarios.add(request.user)  # El admin se une automáticamente
            return redirect('lista_grupos')
    else:
        form = GrupoForm()
    return render(request, 'crear_grupo.html', {'form': form})

def lista_grupos(request):
    grupos = Grupo.objects.all()
    query = request.GET.get('q')
    if query:
        grupos = grupos.filter(nombre__icontains=query)
    return render(request, 'lista_grupos.html', {'grupos': grupos})

def detalles_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    mensajes = grupo.mensajes.all().order_by('fecha_creacion')
    form = MensajeGrupoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        mensaje = form.save(commit=False)
        mensaje.grupo = grupo
        mensaje.usuario = request.user
        mensaje.save()
        return redirect('detalles_grupo', grupo_id=grupo.id)
    return render(request, 'detalles_grupo.html', {'grupo': grupo, 'mensajes': mensajes, 'form': form})

@login_required
def unirse_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)

    # Si el grupo es público, añadir al usuario
    if grupo.tipo == 'publico':
        grupo.usuarios.add(request.user)
        messages.success(request, 'Te has unido al grupo exitosamente.')
    else:
        # Si es por invitación, crea una solicitud
        if not SolicitudGrupo.objects.filter(grupo=grupo, usuario=request.user).exists():
            SolicitudGrupo.objects.create(grupo=grupo, usuario=request.user)
            messages.info(request, 'Tu solicitud de unión ha sido enviada. Espera la aprobación del administrador.')
        else:
            messages.warning(request, 'Ya has enviado una solicitud para unirte a este grupo.')

    return redirect('detalles_grupo', grupo_id=grupo.id)

@login_required
def solicitar_union_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)

    # Verificar si el grupo es por invitación
    if grupo.tipo == 'invitacion':
        # Evitar solicitudes duplicadas
        if not SolicitudGrupo.objects.filter(grupo=grupo, usuario=request.user).exists():
            SolicitudGrupo.objects.create(grupo=grupo, usuario=request.user)
            messages.info(request, 'Tu solicitud de unión ha sido enviada. Espera la aprobación del administrador.')
        else:
            messages.warning(request, 'Ya has enviado una solicitud para unirte a este grupo.')
    else:
        messages.error(request, 'Este grupo es público. Únete directamente desde la página de detalles del grupo.')

    return redirect('detalles_grupo', grupo_id=grupo.id)

@login_required
def gestionar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)

    # Verificar que el usuario es el administrador del grupo
    if request.user != grupo.admin:
        messages.error(request, 'No tienes permiso para administrar este grupo.')
        return redirect('detalles_grupo', grupo_id=grupo.id)

    solicitudes = SolicitudGrupo.objects.filter(grupo=grupo)

    if request.method == 'POST':
        accion = request.POST.get('accion')
        usuario_id = request.POST.get('usuario_id')

        # Manejar la aceptación/rechazo de solicitudes
        if usuario_id:
            solicitud = get_object_or_404(SolicitudGrupo, id=usuario_id)
            if accion == 'aceptar':
                grupo.usuarios.add(solicitud.usuario)
                solicitud.delete()
                messages.success(request, f"{solicitud.usuario.username} ha sido añadido al grupo.")
            elif accion == 'rechazar':
                solicitud.delete()
                messages.info(request, f"Has rechazado la solicitud de {solicitud.usuario.username}.")
        
        # Manejar la expulsión de usuarios
        elif accion == 'expulsar':
            usuario = get_object_or_404(User, id=usuario_id)
            grupo.usuarios.remove(usuario)
            messages.info(request, f"{usuario.username} ha sido expulsado del grupo.")

    return render(request, 'gestionar_grupo.html', {
        'grupo': grupo,
        'solicitudes': solicitudes,
        'usuarios': grupo.usuarios.all(),
    })

@login_required
def eliminar_mensaje_grupo(request, mensaje_id):
    mensaje = get_object_or_404(MensajeGrupo, pk=mensaje_id)
    
    # Verificar que el usuario sea el administrador del grupo
    if request.user == mensaje.grupo.admin:
        mensaje.delete()
        messages.success(request, 'Mensaje eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este mensaje.')
    
    return redirect('detalles_grupo', grupo_id=mensaje.grupo.id)

@login_required
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)

    # Verificar que el usuario es el administrador
    if request.user != grupo.admin:
        messages.error(request, 'No tienes permiso para eliminar este grupo.')
        return redirect('detalles_grupo', grupo_id=grupo.id)

    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'El grupo ha sido eliminado.')
        return redirect('lista_grupos')

    return render(request, 'confirmar_eliminar_grupo.html', {'grupo': grupo})

@login_required
def perfil(request):
    perfil_usuario = request.user.perfilusuario
    historial_compras = Pedido.objects.filter(usuario=request.user)
    grupos_creados = Grupo.objects.filter(admin=request.user)
    
    return render(request, 'perfil.html', {
        'perfil_usuario': perfil_usuario,
        'historial_compras': historial_compras,
        'grupos_creados': grupos_creados,
    })

@login_required
def editar_perfil(request):
    perfil_usuario = request.user.perfilusuario
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')  # Redirige al perfil del usuario después de guardar
    else:
        form = PerfilForm(instance=perfil_usuario)
    
    return render(request, 'editar_perfil.html', {'form': form})
                
@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # Redirige al inicio tras eliminar la cuenta
    return render(request, 'confirmar_eliminar_cuenta.html')
