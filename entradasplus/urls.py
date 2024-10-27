# ---------------------------------------------------------
#                       IMPORTS
# ---------------------------------------------------------

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

# ---------------------------------------------------------
#                    SECCION URLPATTERNS
# ---------------------------------------------------------

urlpatterns = [
    # -----------------------------------------------------
    #                  SECCION PÁGINA PRINCIPAL
    # -----------------------------------------------------
    path('', views.index, name='home'),
    path('calendar', views.calendar, name='calendar'),
    path('trending/', views.trending, name='trending'),
    path('colaboradores/', views.colaboradores),

    # -----------------------------------------------------
    #            SECCION INICIO Y CIERRE DE SESIÓN
    # -----------------------------------------------------
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('login_empresa/', views.login_empresa, name='login_empresa'),

    # -----------------------------------------------------
    #                   SECCION REGISTRO
    # -----------------------------------------------------
    path("register/", views.register, name="register"),
    path('contacta-con-nosotros/', views.contactar_empresa, name='contactar_empresa'),
    path('empresa/pendiente/', views.empresa_pendiente),

    # -----------------------------------------------------
    #                     SECCION EMPRESA
    # -----------------------------------------------------
    path('mi_empresa/', views.miEmpresa),

    # -----------------------------------------------------
    #                     SECCION EVENTOS
    # -----------------------------------------------------
    path('comprar/<int:evento_id>/', views.comprar, name='comprar'),  # Selección de entradas
    path('comprar_evento/<int:evento_id>/', views.comprar_evento, name='comprar_evento'),  # Confirmación de compra
    path('evento/<int:evento_id>/chat/', views.chat_evento, name='chat_evento'),

    # -----------------------------------------------------
    #                      SECCION GRUPOS
    # -----------------------------------------------------
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupos/<int:grupo_id>/', views.detalles_grupo, name='detalles_grupo'),
    path('grupos/<int:grupo_id>/unirse/', views.unirse_grupo, name='unirse_grupo'),
    path('grupos/<int:grupo_id>/solicitar_union/', views.solicitar_union_grupo, name='solicitar_union_grupo'),
    path('grupos/<int:grupo_id>/gestionar/', views.gestionar_grupo, name='gestionar_grupo'),
    path('grupos/mensajes/<int:mensaje_id>/eliminar/', views.eliminar_mensaje_grupo, name='eliminar_mensaje_grupo'),
    path('grupos/<int:grupo_id>/eliminar/', views.eliminar_grupo, name='eliminar_grupo'),
    path('grupos/<int:grupo_id>/cancelar_solicitud/', views.cancelar_solicitud_grupo, name='cancelar_solicitud_grupo'),
    # -----------------------------------------------------
    #                  SECCION PERFIL DEL USUARIO
    # -----------------------------------------------------
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/eliminar/', views.eliminar_cuenta, name='eliminar_cuenta'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ---------------------------------------------------------
#              SERVICIOS ESTÁTICOS EN MODO DEBUG
# ---------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
