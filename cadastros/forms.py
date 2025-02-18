from django import forms
from .models import Agendamento
from .models import Servico

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