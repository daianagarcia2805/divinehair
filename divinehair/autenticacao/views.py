from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        senha = request.POST.get("senha")

        user = authenticate(request, username=email, password=senha)

        if user is not None:
            login(request, user)
            return redirect("core:main")  # Redireciona para a tela principal
        else:
            messages.error(request, "E-mail ou senha inválidos!")

    return render(request, "autenticacao/login.html")

def logout_view(request):
    logout(request)
    return redirect("autenticacao:login")
