from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    email = models.EmailField(blank=True)  # Correo electrónico único
    password = models.CharField(blank=True,max_length=128)  # Contraseña encriptada
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Evento(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)  # Empresa organizadora
    fecha_evento = models.DateTimeField()  # Fecha del evento
    lugar = models.CharField(max_length=200)
    capacidad = models.IntegerField()  # Capacidad máxima del evento
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Entrada(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='entradas')  # Evento al que pertenece la entrada
    tipo = models.CharField(max_length=50)  # Ej: General, VIP, etc.
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField()  # Cantidad de entradas disponibles
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo} - {self.evento.nombre}'
    
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Usuario que hace la compra
    entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE)  # Entrada comprada
    cantidad = models.IntegerField()  # Cantidad de entradas compradas
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Total de la compra

    def __str__(self):
        return f'Pedido de {self.usuario.username} - {self.entrada.evento.nombre}'

class Reseña(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.IntegerField()  # Rango de 1 a 5, por ejemplo
    fecha_creacion = models.DateTimeField(auto_now_add=True)

