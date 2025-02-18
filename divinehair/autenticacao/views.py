from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomLoginForm
from .decorators import perfil_required

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Verificar o perfil do usuário e redirecionar
            if user.tem_perfil('admin'):
                return redirect('autenticacao:admin_dashboard')  # Página de administração
            elif user.tem_perfil('funcionario'):
                return redirect('autenticacao:funcionario_dashboard')  # Página de funcionário
            else:
                return redirect('autenticacao:cliente_dashboard')  # Página de cliente
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = CustomLoginForm()

    return render(request, 'autenticacao/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect("autenticacao:login")

@perfil_required('admin')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@perfil_required('funcionario')
def funcionario_dashboard(request):
    return render(request, 'autenticacao/funcionario_dashboard.html')

@perfil_required('cliente')
def cliente_dashboard(request):
    return render(request, 'autenticacao/cliente_dashboard.html')

@perfil_required('Admin')
def admin_dashboard(request):
    return render(request, 'autenticacao/admin_dashboard.html')








