from django.shortcuts import render, redirect, get_object_or_404
from .models import Agendamento
from .forms import AgendamentoForm
from django.contrib.auth.decorators import login_required
from .models import Servico
from .forms import ServicoForm
from .models import Usuario
from .forms import UsuarioForm
from .forms import PerfilForm
from django.contrib import messages  # Importar o sistema de mensagens
from .models import Usuario
from .forms import UsuarioForm

@login_required
def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all()
    return render(request, 'agendamentos/lista_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def cria_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:lista_agendamentos')
    else:
        form = AgendamentoForm()
    return render(request, 'agendamentos/form_agendamento.html', {'form': form})

@login_required
def edita_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('cadastros:lista_agendamentos')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'agendamentos/form_agendamento.html', {'form': form})

@login_required
def deleta_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        agendamento.delete()
        return redirect('cadastros:lista_agendamentos')
    return render(request, 'agendamentos/confirm_deletar.html', {'agendamento': agendamento})


# Listar serviços
# Listar serviços
def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos/listar_servicos.html', {'servicos': servicos})

# Criar novo serviço
def criar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:listar_servicos')  # Redireciona após criar o serviço
    else:
        form = ServicoForm()
    return render(request, 'servicos/criar_servico.html', {'form': form})

# Editar serviço
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('cadastros:listar_servicos')  # Redireciona após salvar
    else:
        form = ServicoForm(instance=servico)
    
    return render(request, 'servicos/editar_servico.html', {'form': form})

# Deletar serviço
def deletar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        servico.delete()
        return redirect('cadastros:listar_servicos')  # Corrigido para 'listar_servicos'
    
    return render(request, 'servicos/confirm_deletar_servico.html', {'servico': servico})


# View para listar os usuários
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('cadastros:listar_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/criar_usuario.html', {'form': form})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            # Adicionar uma mensagem de sucesso
            messages.success(request, 'Usuário alterado com sucesso!')
            return redirect('cadastros:listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

# View para excluir um usuário
def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('cadastros:listar_usuarios')  # Certifique-se de que o nome está correto
    return render(request, 'usuarios/excluir_usuario.html', {'usuario': usuario})