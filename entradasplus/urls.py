from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('calendar', views.calendar, name='calendar'),
    path('login', views.login_view, name='login'),
    path('eventos/<int:evento_id>/', views.detalles_evento, name='detalles_evento'),
     path('logout/', views.logout_view, name='logout')
    #path('comprar/<int:entrada_id>/', views.comprar_entrada, name='comprar_entrada'),
    #path('grupos/', views.grupos, name='grupos'),
    #path('perfil/', views.perfil, name='perfil')
]

