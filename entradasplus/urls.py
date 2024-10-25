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
    path('empresa/pendiente/', views.empresa_pendiente)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

