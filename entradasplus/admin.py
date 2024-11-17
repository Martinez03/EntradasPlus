from django.contrib import admin
from .models import Empresa, Evento, Entrada, Pedido, PerfilUsuario, Grupo, MensajeCalendario

admin.site.register(Evento)
admin.site.register(Entrada)
admin.site.register(Pedido)
admin.site.register(PerfilUsuario)
admin.site.register(Grupo)
admin.site.register(MensajeCalendario)


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'estado')  
    list_filter = ('estado',)  