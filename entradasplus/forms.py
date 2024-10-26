from django import forms
from .models import Evento,Empresa, Mensaje
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_evento', 'lugar', 'capacidad']

class EmpresaForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Nombre de usuario para iniciar sesión")
    password = forms.CharField(widget=forms.PasswordInput, help_text="Contraseña")
    email_usuario = forms.EmailField(help_text="Email para la cuenta de usuario")

    class Meta:
        model = Empresa
        fields = ['nombre', 'email', 'telefono', 'direccion']  # Campos de la empresa

    def save(self, commit=True):
        # Sobrescribimos el método save para crear el usuario junto con la empresa
        empresa = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email_usuario']
        )
        empresa.usuario = user  # Asociar el usuario a la empresa
        if commit:
            empresa.save()
        return empresa

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Escribe un mensaje...'}),
        }
