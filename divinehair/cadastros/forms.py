from django import forms
from .models import Agendamento, Servico, Usuario, Perfil

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['usuario', 'servico', 'data_hora', 'status']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        # retira o usuário dos kwargs, se fornecido
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None and user.tem_perfil('cliente'):
            # se for cliente, restringe o campo "usuario" apenas ao próprio usuário
            self.fields['usuario'].queryset = Usuario.objects.filter(pk=user.pk)
            # define o valor inicial para o próprio usuário
            self.fields['usuario'].initial = user.pk
            # oculta o campo (campo oculto)
            self.fields['usuario'].widget = forms.HiddenInput()
            # desativa a obrigatoriedade, pois o valor inicial já está definido
            self.fields['usuario'].required = False
        else:
            # para administradores e funcionários, mostra todos os usuários
            self.fields['usuario'].queryset = Usuario.objects.all()


class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco']


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # campo de senha

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'password', 'is_active', 'is_admin', 'perfis', 'servicos']
        widgets = {
            'perfis': forms.CheckboxSelectMultiple(),  # permite selecionar múltiplos perfis
            'servicos': forms.CheckboxSelectMultiple(),  # permite selecionar múltiplos serviços
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['perfis'].queryset = Perfil.objects.all()  # permite escolher os perfis
        self.fields['servicos'].queryset = Servico.objects.all()  # permite escolher os serviços

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # criptografa a senha
        if commit:
            user.save()
            self.save_m2m()  # salva as relações ManyToMany
        return user


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nome']
