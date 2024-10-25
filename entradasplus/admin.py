from django.contrib import admin
from .models import Empresa, Evento, Entrada, Pedido, PerfilUsuario

admin.site.register(Evento)
admin.site.register(Entrada)
admin.site.register(Pedido)
admin.site.register(PerfilUsuario)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'estado')  # Mostrar estos campos en el admin
    list_filter = ('estado',)  # Filtrar por estado