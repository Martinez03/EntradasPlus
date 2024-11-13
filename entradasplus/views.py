# ---------------------------------------------------------
#                       IMPORTS
# ---------------------------------------------------------

from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Q
from datetime import datetime

from .models import Entrada, Empresa, Evento, Mensaje, Pedido, Grupo, PerfilUsuario, SolicitudGrupo, MensajeGrupo, MensajeCalendario
from .forms import EventoForm, EmpresaForm, RegisterForm, MensajeForm, PerfilForm, GrupoForm, MensajeGrupoForm, EditarEmpresaForm, EditarEventoForm, MensajeCalendarioForm
from .decorators import empresa_verificada_required
from django.contrib.admin.views.decorators import staff_member_required
import calendar
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# ---------------------------------------------------------
#                  SECCION PÁGINA PRINCIPAL
# ---------------------------------------------------------

def index(request):
    entradas = Entrada.objects.filter(evento__fecha_evento__gte=timezone.now()).order_by('evento__fecha_evento')
    user_empresa = False
    if request.user.is_authenticated:
        try:
            user_empresa = Empresa.objects.filter(usuario=request.user).exists()
        except Empresa.DoesNotExist:
            user_empresa = False
    return render(request, 'index.html', {
        'entradas': entradas,
        'user_empresa': user_empresa
    })

def calendar_view(request, year=None, month=None):
    
    today = datetime.today()
    year = year or today.year
    month = month or today.month
    current_day = today.day if (today.year == year and today.month == month) else None

    
    month_name = datetime(year, month, 1).strftime('%B')

    
    cal = calendar.Calendar(firstweekday=0)  
    days = [day for week in cal.monthdayscalendar(year, month) for day in week]
    
     
    eventos_mes = Evento.objects.filter(fecha_evento__year=year, fecha_evento__month=month)
    
    
    eventos_por_dia = {}
    for evento in eventos_mes:
        dia_evento = evento.fecha_evento.day
        if dia_evento not in eventos_por_dia:
            eventos_por_dia[dia_evento] = evento.nombre  

 
    days_with_events = [
        {
            "day": day,
            "event": eventos_por_dia.get(day, ""),  # Primer evento o vacío
            "is_today": (day == current_day) if day != 0 else False,
            "is_empty": (day == 0)
        }
        for day in days
    ]
    

    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1

    return render(request, "calendar.html", {
        "days_with_events": days_with_events,
        "month_name": month_name.capitalize(),
        "year": year,
        "month": month,
        "next_month": next_month,
        "next_year": next_year,
        "prev_month": prev_month,
        "prev_year": prev_year,
    })

def day_events_view(request, year, month, day):
    selected_date = datetime(year, month, day)
    eventos_del_dia = Evento.objects.filter(fecha_evento__date=selected_date.date())

    # Obtener los mensajes del día
    mensajes_del_dia = MensajeCalendario.objects.filter(dia=selected_date.date()).order_by('fecha_creacion')

    # Manejo del formulario para nuevos mensajes
    if request.method == "POST":
        form = MensajeCalendarioForm(request.POST)
        if form.is_valid():
            # Guardar el mensaje solo si el formulario es válido
            MensajeCalendario.objects.create(
                dia=selected_date.date(),
                usuario=request.user,
                contenido=form.cleaned_data['contenido']
            )
            return redirect('day_events_view', year=year, month=month, day=day)  # Redirigir para evitar reenvío del formulario

    else:
        form = MensajeCalendarioForm()

    return render(request, "calendario_dia.html", {
        "eventos": eventos_del_dia,
        "selected_date": selected_date.strftime("%d de %B de %Y"),
        "mensajes": mensajes_del_dia,
        "form": form,  # Pasar el formulario al template
    })


def colaboradores(request):
    empresas = Empresa.objects.filter(estado='verificada')
    return render(request, 'colaboradores.html',{'empresas': empresas})

# ---------------------------------------------------------
#            SECCION INICIO Y CIERRE DE SESIÓN
# ---------------------------------------------------------

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return redirect('home')
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def login_empresa(request):
    return render(request, 'index.html')

# ---------------------------------------------------------
#                  SECCION REGISTRO
# ---------------------------------------------------------

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardar el usuario
            messages.success(request, '¡Registro exitoso! Has iniciado sesión automáticamente.')
            
            # Iniciar sesión automáticamente
            login(request, user)
            return redirect('/')  # Cambia '/' a la página que desees mostrar después del login
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
        
def contactar_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('empresa_pendiente')
    else:
        form = EmpresaForm()
    return render(request, 'contactar_empresa.html', {'form': form})

# ---------------------------------------------------------
#                  SECCION EMPRESA
# ---------------------------------------------------------

def miEmpresa(request):
    if request.user.is_authenticated:
        user_empresa = True
        empresa = Empresa.objects.get(usuario=request.user)   
        eventos = Evento.objects.filter(empresa=empresa) 
    return render(request, 'mi_empresa.html', {
        'empresa': empresa,
        'user_empresa': user_empresa,
        'eventos': eventos,
        'user_empresa': True
    })

def verificar_estado_empresa(user):
    try:
        empresa = Empresa.objects.get(usuario=user)
        return empresa.estado != 'pendiente'
    except Empresa.DoesNotExist:
        return True

def empresa_pendiente(request):
    return render(request, 'empresa_pendiente.html')

@staff_member_required
def admin_empresas_pendientes(request):
    empresas_pendientes = Empresa.objects.filter(estado='pendiente')
    return render(request, 'admin_empresas_pendientes.html', {'empresas_pendientes': empresas_pendientes})

@staff_member_required
def verificar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    if request.method == 'POST':
        empresa.estado = 'verificada'
        empresa.save()
        messages.success(request, f'La empresa {empresa.nombre} ha sido verificada.')
        return redirect('admin_empresas_pendientes')
    return render(request, 'verificar_empresa.html', {'empresa': empresa})

@empresa_verificada_required
def editar_empresa(request):
    empresa = get_object_or_404(Empresa, usuario=request.user)

    if request.method == 'POST':
        form = EditarEmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información de la empresa actualizada exitosamente.')
            return redirect('mi_empresa')
    else:
        form = EditarEmpresaForm(instance=empresa)
    
    return render(request, 'editar_empresa.html', {'form': form, 'user_empresa': True})


def lista_empresas_verificadas(request):
    empresas = Empresa.objects.filter(estado='verificada')
    return render(request, 'colaboradores.html', {'empresas': empresas})

def detalle_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, estado='verificada')
    eventos = Evento.objects.filter(empresa=empresa)
    return render(request, 'detalle_empresa.html', {'empresa': empresa, 'eventos': eventos})

# ---------------------------------------------------------
#                  SECCION EVENTOS
# ---------------------------------------------------------

@empresa_verificada_required
def crear_evento(request):
    empresa = Empresa.objects.get(usuario=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.empresa = empresa
            evento.save()
            return redirect('mi_empresa')
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form, 'user_empresa': True})

@empresa_verificada_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, empresa__usuario=request.user)
    if request.method == 'POST':
        form = EditarEventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado exitosamente.')
            return redirect('mis_eventos')
    else:
        form = EditarEventoForm(instance=evento)
    return render(request, 'events/editar_evento.html', {'form': form, 'evento': evento})

@empresa_verificada_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, empresa__usuario=request.user)
    if request.method == 'POST':
        evento.delete()
        messages.success(request, 'Evento eliminado exitosamente.')
        return redirect('mis_eventos')
    return render(request, 'events/confirmar_eliminar_evento.html', {'evento': evento})

@empresa_verificada_required
def compradores_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, empresa__usuario=request.user)
    pedidos = Pedido.objects.filter(entrada__evento=evento).select_related('usuario')
    return render(request, 'events/compradores_evento.html', {'evento': evento, 'pedidos': pedidos})


def trending(request):
    eventos = Evento.objects.all()
    return render(request, 'trending.html', {'eventos': eventos})

def comprar(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    entradas = evento.entradas.all()
    return render(request, 'comprar.html', {'evento': evento, 'entradas': entradas})

def comprar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    perfil_usuario = PerfilUsuario.objects.get(user=request.user)
    if request.method == 'POST':
        entrada_id = request.POST.get('entrada_id')
        cantidad = int(request.POST.get('cantidad', 1))
        entrada = get_object_or_404(Entrada, id=entrada_id)
        total = cantidad * entrada.precio
        if cantidad > entrada.cantidad_disponible:
            messages.error(request, f'Solo quedan {entrada.cantidad_disponible} entradas disponibles.')
            return redirect('comprar', evento_id=evento.id)
        if perfil_usuario.dinero < total:
            messages.error(request, f'No tienes suficiente dinero. Te faltan {total - perfil_usuario.dinero}€.')
            return redirect('comprar', evento_id=evento.id)
        entrada.cantidad_disponible -= cantidad
        perfil_usuario.dinero -= total
        entrada.save()
        perfil_usuario.save()
        Pedido.objects.create(
            usuario=request.user,
            entrada=entrada,
            cantidad=cantidad,
            fecha_compra=timezone.now(),
            total=total
        )
        messages.success(request, '¡Compra realizada con éxito!')
        return redirect('comprar', evento_id=evento.id)
    return redirect('comprar', evento_id=evento.id)

@empresa_verificada_required
def mis_eventos(request):
    empresa = Empresa.objects.get(usuario=request.user)
    eventos = Evento.objects.filter(empresa=empresa)
    return render(request, 'mis_eventos.html', {'eventos': eventos})


# ---------------------------------------------------------
#                  SECCION CHAT DE EVENTOS
# ---------------------------------------------------------

def chat_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    mensajes = evento.mensajes.order_by('fecha_creacion')
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.evento = evento
            mensaje.usuario = request.user
            mensaje.save()
            return redirect('chat_evento', evento_id=evento_id)
    else:
        form = MensajeForm()
    return render(request, 'chat_evento.html', {'evento': evento, 'mensajes': mensajes, 'form': form})

# ---------------------------------------------------------
#                  SECCION GRUPOS
# ---------------------------------------------------------

@login_required
def crear_grupo(request):
    if Grupo.objects.filter(admin=request.user).count() >= 3:
        messages.warning(request, 'Has alcanzado el límite de 3 grupos.')
        return redirect('lista_grupos')
    if request.method == 'POST':
        form = GrupoForm(request.POST, request.FILES)
        if form.is_valid():
            grupo = form.save(commit=False)
            grupo.admin = request.user
            grupo.save()
            grupo.usuarios.add(request.user)
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

@login_required
def detalles_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    
    # Verificar si el usuario ya tiene una solicitud de unión pendiente
    solicitud_pendiente = SolicitudGrupo.objects.filter(grupo=grupo, usuario=request.user).exists()

    # Si el usuario está en el grupo, obtener los mensajes
    if request.user in grupo.usuarios.all() or request.user == grupo.admin:
        mensajes = grupo.mensajes.all().order_by('fecha_creacion')
        form = MensajeGrupoForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.grupo = grupo
            mensaje.usuario = request.user
            mensaje.save()
            return redirect('detalles_grupo', grupo_id=grupo.id)
    else:
        # Si el usuario no es miembro y no tiene una solicitud pendiente, mostrar opciones de unirse
        mensajes = None  # No mostrar mensajes si no está en el grupo
        form = None  # No mostrar formulario de mensaje si no está en el grupo
    
    return render(request, 'detalles_grupo.html', {
        'grupo': grupo,
        'mensajes': mensajes,
        'form': form,
        'solicitud_pendiente': solicitud_pendiente
    })

@login_required
def unirse_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    if grupo.tipo == 'publico':
        grupo.usuarios.add(request.user)
        messages.success(request, 'Te has unido al grupo exitosamente.')
    else:
        if not SolicitudGrupo.objects.filter(grupo=grupo, usuario=request.user).exists():
            SolicitudGrupo.objects.create(grupo=grupo, usuario=request.user)
            messages.info(request, 'Tu solicitud de unión ha sido enviada.')
        else:
            messages.warning(request, 'Ya has enviado una solicitud para unirte a este grupo.')
    return redirect('detalles_grupo', grupo_id=grupo.id)

@login_required
def solicitar_union_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    if grupo.tipo == 'invitacion':
        if not SolicitudGrupo.objects.filter(grupo=grupo, usuario=request.user).exists():
            SolicitudGrupo.objects.create(grupo=grupo, usuario=request.user)
            messages.info(request, 'Tu solicitud de unión ha sido enviada.')
        else:
            messages.warning(request, 'Ya has enviado una solicitud para unirte a este grupo.')
    else:
        messages.error(request, 'Este grupo es público. Únete directamente desde la página de detalles del grupo.')
    return redirect('detalles_grupo', grupo_id=grupo.id)

@login_required
def gestionar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    if request.user != grupo.admin:
        messages.error(request, 'No tienes permiso para administrar este grupo.')
        return redirect('detalles_grupo', grupo_id=grupo.id)
    
    solicitudes = SolicitudGrupo.objects.filter(grupo=grupo)
    if request.method == 'POST':
        accion = request.POST.get('accion')
        usuario_id = request.POST.get('usuario_id')
        
        if accion == 'expulsar' and int(usuario_id) == request.user.id:
            messages.warning(request, 'No puedes expulsarte a ti mismo. Si deseas eliminar el grupo, confirma la eliminación.')
            return redirect('eliminar_grupo', grupo_id=grupo.id)

        if usuario_id:
            solicitud = get_object_or_404(SolicitudGrupo, id=usuario_id)
            if accion == 'aceptar':
                grupo.usuarios.add(solicitud.usuario)
                solicitud.delete()
                messages.success(request, f"{solicitud.usuario.username} ha sido añadido al grupo.")
            elif accion == 'rechazar':
                solicitud.delete()
                messages.info(request, f"Has rechazado la solicitud de {solicitud.usuario.username}.")
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
    if request.user == mensaje.grupo.admin:
        mensaje.delete()
        messages.success(request, 'Mensaje eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este mensaje.')
    return redirect('detalles_grupo', grupo_id=mensaje.grupo.id)

@login_required
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, id=grupo_id)
    if request.user != grupo.admin:
        messages.error(request, 'No tienes permiso para eliminar este grupo.')
        return redirect('detalles_grupo', grupo_id=grupo.id)
    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'El grupo ha sido eliminado.')
        return redirect('lista_grupos')
    return render(request, 'confirmar_eliminar_grupo.html', {'grupo': grupo})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def cancelar_solicitud_grupo(request, grupo_id):
    grupo = get_object_or_404(Grupo, pk=grupo_id)
    solicitud = SolicitudGrupo.objects.filter(grupo=grupo, usuario=request.user).first()

    if solicitud:
        solicitud.delete()
        messages.info(request, 'Tu solicitud de unión ha sido cancelada.')
    else:
        messages.warning(request, 'No tienes una solicitud pendiente para este grupo.')

    return redirect('detalles_grupo', grupo_id=grupo.id)

# ---------------------------------------------------------
#                  SECCION PERFIL DEL USUARIO
# ---------------------------------------------------------

@login_required
def perfil(request):
    perfil_usuario = request.user.perfilusuario
    historial_compras = Pedido.objects.filter(usuario=request.user)
    grupos_creados = Grupo.objects.filter(admin=request.user)
    user_empresa = False
    if request.user.is_authenticated:
        try:
            user_empresa = Empresa.objects.filter(usuario=request.user).exists()
        except Empresa.DoesNotExist:
            user_empresa = False
    return render(request, 'perfil.html', {
        'perfil_usuario': perfil_usuario,
        'historial_compras': historial_compras,
        'grupos_creados': grupos_creados,
        'user_empresa':user_empresa
    })

@login_required
def editar_perfil(request):
    perfil_usuario = request.user.perfilusuario
    user_empresa = False
    if request.user.is_authenticated:
        try:
            user_empresa = Empresa.objects.filter(usuario=request.user).exists()
        except Empresa.DoesNotExist:
            user_empresa = False
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil_usuario)
    return render(request, 'editar_perfil.html', {'form': form, 'user_empresa':user_empresa})

@login_required
def eliminar_cuenta(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')
    return render(request, 'confirmar_eliminar_cuenta.html')
