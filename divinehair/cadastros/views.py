from django.shortcuts import render, redirect, get_object_or_404
from .models import Agendamento
from .forms import AgendamentoForm
from django.contrib.auth.decorators import login_required
from .models import Servico
from .forms import ServicoForm
from .models import Usuario
from .forms import UsuarioForm
from .forms import PerfilForm
from django.contrib import messages  
from .models import Usuario
from .forms import UsuarioForm

@login_required
def lista_agendamentos(request):
    # obtém todos os perfis do usuário
    perfis_usuario = request.user.perfis.values_list('nome', flat=True)

    if "cliente" in perfis_usuario and "admin" not in perfis_usuario and "funcionario" not in perfis_usuario:
        # se o usuário for APENAS cliente, ele vê apenas seus próprios agendamentos
        agendamentos = Agendamento.objects.filter(usuario=request.user)
    else:
        # caso contrário, se for funcionário ou admin, vê todos os agendamentos
        agendamentos = Agendamento.objects.all()

    return render(request, 'agendamentos/lista_agendamentos.html', {'agendamentos': agendamentos})

@login_required
def cria_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, user=request.user)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user  # atribui o usuário logado ao agendamento
            agendamento.save()
            # redireciona com base no perfil do usuário:
            if request.user.tem_perfil('admin'):
                return redirect('autenticacao:admin_dashboard')
            elif request.user.tem_perfil('funcionario'):
                return redirect('autenticacao:funcionario_dashboard')
            else:
                return redirect('autenticacao:cliente_dashboard')
    else:
        form = AgendamentoForm(user=request.user)
    return render(request, 'agendamentos/form_agendamento.html', {'form': form})


@login_required
def edita_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    # verifica se o usuário é cliente e não é o dono do agendamento
    if request.user.tem_perfil('cliente') and agendamento.usuario != request.user:
        messages.error(request, "Você não tem permissão para editar esse agendamento.")
        return redirect('autenticacao:cliente_dashboard')  # redireciona para o dashboard do cliente
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('cadastros:lista_agendamentos')  # para admin ou funcionário, redireciona para lista de agendamentos
    else:
        form = AgendamentoForm(instance=agendamento)
    
    return render(request, 'agendamentos/form_agendamento.html', {'form': form})

@login_required
def deleta_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    # verifica se o usuário é cliente e não é o dono do agendamento
    if request.user.tem_perfil('cliente') and agendamento.usuario != request.user:
        messages.error(request, "Você não tem permissão para excluir esse agendamento.")
        return redirect('autenticacao:cliente_dashboard')  # redireciona para o dashboard do cliente
    
    if request.method == 'POST':
        agendamento.delete()
        return redirect('cadastros:lista_agendamentos')  # para admin ou funcionário, redireciona para lista de agendamentos
    
    return render(request, 'agendamentos/confirm_deletar.html', {'agendamento': agendamento})


# listar serviços
def listar_servicos(request):
    servicos = Servico.objects.all()
    return render(request, 'servicos/listar_servicos.html', {'servicos': servicos})

# criar novo serviço
def criar_servico(request):
    if request.method == 'POST':
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastros:listar_servicos')  # Redireciona após criar o serviço
    else:
        form = ServicoForm()
    return render(request, 'servicos/criar_servico.html', {'form': form})

# editar serviço
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect('cadastros:listar_servicos')  # redireciona após salvar
    else:
        form = ServicoForm(instance=servico)
    
    return render(request, 'servicos/editar_servico.html', {'form': form})

# deletar serviço
def deletar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    
    if request.method == 'POST':
        servico.delete()
        return redirect('cadastros:listar_servicos')  # Corrigido para 'listar_servicos'
    
    return render(request, 'servicos/confirm_deletar_servico.html', {'servico': servico})


# view para listar os usuários
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

def criar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # não salva ainda
            usuario.set_password(form.cleaned_data['password'])  # criptografa a senha
            usuario.save()  
            form.save_m2m()  # salva o relacionamento muitos-para-muitos (serviços)
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
            # adicionar uma mensagem de sucesso
            messages.success(request, 'Usuário alterado com sucesso!')
            return redirect('cadastros:listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})

# view para excluir um usuário
def excluir_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('cadastros:listar_usuarios')  # certifique-se de que o nome está correto
    return render(request, 'usuarios/excluir_usuario.html', {'usuario': usuario})