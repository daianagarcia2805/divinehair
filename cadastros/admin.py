from django.contrib import admin
from .models import Usuario, Perfil

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('email', 'nome', 'is_active', 'is_staff')
    search_fields = ('email', 'nome')
    ordering = ('email',)
    filter_horizontal = ('perfis',)  # Para permitir a seleção de múltiplos perfis de forma mais prática
    
    # Para incluir o campo 'perfis' na tela de edição
    fieldsets = (
        (None, {
            'fields': ('email', 'nome', 'perfis', 'is_active', 'is_admin'),
        }),
    )

admin.site.register(Usuario, UsuarioAdmin)