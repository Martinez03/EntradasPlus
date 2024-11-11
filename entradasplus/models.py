# ---------------------------------------------------------
#                       IMPORTS
# ---------------------------------------------------------

from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# ---------------------------------------------------------
#                  SECCION MODELOS EMPRESA
# ---------------------------------------------------------

class Empresa(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('verificada', 'Verificada'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')  
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 

    def __str__(self):
        return self.nombre

# ---------------------------------------------------------
#                  SECCION MODELOS EVENTOS
# ---------------------------------------------------------

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha_evento = models.DateTimeField()
    lugar = models.CharField(max_length=200)
    capacidad = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Entrada(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='entradas')
    tipo = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.evento.nombre}'

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pedido de {self.usuario.username} - {self.entrada.evento.nombre}'

class Reseña(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

# ---------------------------------------------------------
#                SECCION MODELO PERFIL USUARIO
# ---------------------------------------------------------

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/people.png', null=True, blank=True)
    dinero = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)
    eventos_con_like = models.ManyToManyField('Evento', related_name='usuarios_con_like', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

# ---------------------------------------------------------
#                  SECCION MODELOS MENSAJES
# ---------------------------------------------------------

class Mensaje(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='mensajes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.evento.nombre}"

# ---------------------------------------------------------
#                  SECCION MODELOS GRUPOS
# ---------------------------------------------------------

class Grupo(models.Model):
    NOMBRE_MAX_LENGTH = 100
    TIPO_GRUPO_CHOICES = [
        ('publico', 'Público'),
        ('invitacion', 'Por Invitación'),
    ]

    nombre = models.CharField(max_length=NOMBRE_MAX_LENGTH)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_GRUPO_CHOICES, default='publico')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grupos_admin')
    usuarios = models.ManyToManyField(User, related_name='grupos', blank=True)
    foto = models.ImageField(upload_to='grupos/', default='grupos/default.webp', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class SolicitudGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='solicitudes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

class MensajeGrupo(models.Model):
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, related_name='mensajes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.grupo.nombre}"

# ---------------------------------------------------------
#              SECCION SEÑALES (SIGNALS)
# ---------------------------------------------------------

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.perfilusuario.save()
