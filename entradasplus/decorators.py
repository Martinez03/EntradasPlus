from django.shortcuts import redirect
from .models import Empresa

def empresa_verificada_required(function):
    def wrap(request, *args, **kwargs):
        try:
            empresa = Empresa.objects.get(usuario=request.user)
            if empresa.estado != 'verificada':
                return redirect('empresa_pendiente')  # Redirigir a la página de pendiente
        except Empresa.DoesNotExist:
            return redirect('home')  # Si no es una empresa, redirige a la página principal
        return function(request, *args, **kwargs)
    return wrap
