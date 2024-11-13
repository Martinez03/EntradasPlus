# ---------------------------------------------------------
#                       IMPORTS
# ---------------------------------------------------------

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reseña, Evento, Empresa, Mensaje, Grupo, SolicitudGrupo, MensajeGrupo, PerfilUsuario, MensajeCalendario
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import AdminSplitDateTime

# ---------------------------------------------------------
#                  SECCION FORMULARIOS DE EVENTO
# ---------------------------------------------------------

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_evento', 'lugar', 'capacidad', 'imagen']
        date = forms.DateField()
        widgets = {
            'fecha_evento':forms.TextInput(attrs={'type':'datetime-local'}),
        }
class EditarEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nombre', 'descripcion', 'fecha_evento', 'lugar', 'capacidad', 'imagen']

# ---------------------------------------------------------
#                  SECCION FORMULARIO DE EMPRESA
# ---------------------------------------------------------

class EmpresaForm(forms.ModelForm):
    username = forms.CharField(max_length=150, help_text="Nombre de usuario para iniciar sesión")
    password = forms.CharField(widget=forms.PasswordInput, help_text="Contraseña")
    email_usuario = forms.EmailField(help_text="Email para la cuenta de usuario")

    class Meta:
        model = Empresa
        fields = ['nombre', 'email', 'telefono', 'direccion']

    def save(self, commit=True):
        empresa = super().save(commit=False)
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email_usuario']
        )
        empresa.usuario = user
        if commit:
            empresa.save()
        return empresa

class EditarEmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion', 'email', 'telefono', 'direccion']

# ---------------------------------------------------------
#                SECCION FORMULARIO DE REGISTRO
# ---------------------------------------------------------

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está en uso.")
        return email

# ---------------------------------------------------------
#                 SECCION FORMULARIO DE MENSAJE
# ---------------------------------------------------------

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Escribe un mensaje...'}),
        }


# ---------------------------------------------------------
#                 SECCION FORMULARIO DE CALENDARIO
# ---------------------------------------------------------

class MensajeCalendarioForm(forms.ModelForm):
    class Meta:
        model = MensajeCalendario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Escribe un mensaje...'}),
        }

# ---------------------------------------------------------
#                 SECCION FORMULARIO DE GRUPO
# ---------------------------------------------------------

class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'descripcion', 'tipo', 'foto']

class MensajeGrupoForm(forms.ModelForm):
    class Meta:
        model = MensajeGrupo
        fields = ['contenido']

# ---------------------------------------------------------
#                 SECCION FORMULARIO DE RESEÑA
# ---------------------------------------------------------

class ReseñaForm(forms.ModelForm):
    class Meta:
        model = Reseña
        fields = ['comentario', 'calificacion']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 4}),
            'calificacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

# ---------------------------------------------------------
#               SECCION FORMULARIO DE PERFIL USUARIO
# ---------------------------------------------------------

class PerfilForm(forms.ModelForm):
    nombre = forms.CharField(max_length=30, required=False, label="Nombre")
    apellidos = forms.CharField(max_length=50, required=False, label="Apellidos")
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = PerfilUsuario
        fields = ['avatar', 'dinero', 'descripcion', 'nombre', 'apellidos']

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            # Inicializa el campo de email desde el modelo User
            self.fields['email'].initial = self.instance.user.email
            # Inicializa nombre y apellidos desde el modelo PerfilUsuario
            self.fields['nombre'].initial = self.instance.nombre
            self.fields['apellidos'].initial = self.instance.apellidos

    def save(self, commit=True):
        perfil_usuario = super().save(commit=False)
        
        # Actualiza el email en el modelo User
        if 'email' in self.cleaned_data:
            perfil_usuario.user.email = self.cleaned_data['email']
        
        # Guarda ambos objetos si commit=True
        if commit:
            perfil_usuario.user.save()  # Guarda el email en User
            perfil_usuario.save()       # Guarda el perfil de usuario
        return perfil_usuario