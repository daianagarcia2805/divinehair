from django import forms
from .models import Agendamento
from .models import Servico
from .models import Usuario, Perfil

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['usuario', 'servico', 'data_hora', 'status']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco']

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'perfis', 'servicos', 'is_active', 'is_admin']
        widgets = {
            'perfis': forms.CheckboxSelectMultiple(),
            'servicos': forms.CheckboxSelectMultiple(),
        }

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome']