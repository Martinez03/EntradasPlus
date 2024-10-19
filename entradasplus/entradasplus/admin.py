from django.contrib import admin
from .models import Empresa, Evento, Entrada, Pedido

admin.site.register(Empresa)
admin.site.register(Evento)
admin.site.register(Entrada)
admin.site.register(Pedido)
