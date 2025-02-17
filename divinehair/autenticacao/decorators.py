from django.http import HttpResponseForbidden
from functools import wraps

def perfil_required(perfil_nome):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.tem_perfil(perfil_nome):
                return HttpResponseForbidden("Você não tem permissão para acessar esta página.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
