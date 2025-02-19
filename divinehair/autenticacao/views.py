from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomLoginForm
from .decorators import perfil_required
from cadastros.models import Agendamento
from django.contrib.auth.decorators import login_required
from cadastros.models import Servico

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # verificar o perfil do usuário e redirecionar
            if user.tem_perfil('admin'):
                return redirect('autenticacao:admin_dashboard')  # página de administração
            elif user.tem_perfil('funcionario'):
                return redirect('autenticacao:funcionario_dashboard')  # página de funcionário
            else:
                return redirect('autenticacao:cliente_dashboard')  # página de cliente
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = CustomLoginForm()

    return render(request, 'autenticacao/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("autenticacao:login")

@login_required
@perfil_required('admin')
def admin_dashboard(request):
    agendamentos = Agendamento.objects.all()  # mostrar todos os agendamentos para o admin
    return render(request, 'autenticacao/admin_dashboard.html', {'agendamentos': agendamentos})


@login_required
@perfil_required('funcionario')
def funcionario_dashboard(request):
    agendamentos = Agendamento.objects.all()  # mostrar todos os agendamentos para o funcionário
    servicos = Servico.objects.all()  # obter a lista de serviços
    return render(request, 'autenticacao/funcionario_dashboard.html', {
        'servicos': servicos,
        'agendamentos': agendamentos
    })


@perfil_required('cliente')
def cliente_dashboard(request):
    agendamentos = Agendamento.objects.filter(usuario=request.user)
    print(agendamentos)  # verifique se os agendamentos estão sendo recuperados corretamente
    return render(request, 'autenticacao/cliente_dashboard.html', {'agendamentos': agendamentos})