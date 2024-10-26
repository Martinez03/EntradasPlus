from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   
    path('', views.index, name='home'),
    path('calendar', views.calendar, name='calendar'),
    path('login', views.login_view, name='login'),
    path('eventos/<int:evento_id>/', views.detalles_evento, name='detalles_evento'),
    path('comprar/<int:evento_id>/', views.comprar, name='comprar_evento'),
    path('logout/', views.logout_view, name='logout'),
    path('crear_evento/', views.crear_evento, name='crear_evento'),
    path('editar_evento/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eliminar_evento/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('login_empresa/', views.login_empresa, name='login_empresa'),
    path('trending/', views.trending, name='trending'),
    path("register/", views.register, name="register"),
    path('contacta-con-nosotros/', views.contactar_empresa, name='contactar_empresa'),
    path('empresa/pendiente/', views.empresa_pendiente),
    path('colaboradores/', views.colaboradores),
    path('mi_empresa/', views.miEmpresa),
    path('evento/<int:evento_id>/chat/', views.chat_evento, name='chat_evento'),
    path('grupos/', views.lista_grupos, name='lista_grupos'),
    path('grupos/crear/', views.crear_grupo, name='crear_grupo'),
    path('grupos/<int:grupo_id>/', views.detalles_grupo, name='detalles_grupo'),
    path('grupos/<int:grupo_id>/unirse/', views.unirse_grupo, name='unirse_grupo'),
    path('grupos/<int:grupo_id>/solicitar_union/', views.solicitar_union_grupo, name='solicitar_union_grupo'),
    path('grupos/<int:grupo_id>/gestionar/', views.gestionar_grupo, name='gestionar_grupo'),
    path('grupos/mensajes/<int:mensaje_id>/eliminar/', views.eliminar_mensaje_grupo, name='eliminar_mensaje_grupo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

