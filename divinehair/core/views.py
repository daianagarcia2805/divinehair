
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required  # garante que apenas usuários logados acessem
def home_view(request):
    user = request.user  # obtém o usuário logado

    # redireciona com base no perfil
    if user.tem_perfil('admin'):
        return redirect('autenticacao:admin_dashboard')
    elif user.tem_perfil('funcionario'):
        return redirect('autenticacao:funcionario_dashboard')
    elif user.tem_perfil('cliente'):
        return redirect('autenticacao:cliente_dashboard')

    return render(request, "core/main.html")  # se não tiver perfil, carrega a página padrão

def contato_view(request):
    return render(request, "core/contato.html")  # renderiza o template contato.html