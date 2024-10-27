from django import forms
from .models import Evento, Empresa, Mensaje, Grupo, SolicitudGrupo, MensajeGrupo, PerfilUsuario
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

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'descripcion', 'tipo', 'foto']

class MensajeGrupoForm(forms.ModelForm):
    class Meta:
        model = MensajeGrupo
        fields = ['contenido']

class PerfilForm(forms.ModelForm):
    # Campos adicionales de User
    first_name = forms.CharField(max_length=30, required=False, label="Nombre")
    last_name = forms.CharField(max_length=30, required=False, label="Apellidos")
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = PerfilUsuario
        fields = ['avatar', 'dinero', 'descripcion']  # Campos de PerfilUsuario

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        # Si hay un usuario asociado, inicializamos los datos en los campos adicionales
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        # Guardar los datos del perfil y del usuario
        perfil_usuario = super().save(commit=False)
        perfil_usuario.user.first_name = self.cleaned_data['first_name']
        perfil_usuario.user.last_name = self.cleaned_data['last_name']
        perfil_usuario.user.email = self.cleaned_data['email']
        
        if commit:
            perfil_usuario.user.save()  # Guardar datos del usuario
            perfil_usuario.save()  # Guardar datos del perfil
        return perfil_usuario