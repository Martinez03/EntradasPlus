from django import forms
from .models import Evento,Empresa
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_evento', 'lugar', 'capacidad']

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion', 'email', 'password']



class RegisterForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
