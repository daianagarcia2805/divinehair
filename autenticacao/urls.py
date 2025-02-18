from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from . import views

app_name = "autenticacao"

urlpatterns = [
    # URL de login
    path("login/", views.login_view, name="login"),
    
    # URL de logout
    path("logout/", views.logout_view, name="logout"),
    
    # URLs para diferentes dashboards
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('funcionario/dashboard/', views.funcionario_dashboard, name='funcionario_dashboard'),
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
    
    # URL para alterar senha
    path(
        'alterar_senha/',
        PasswordChangeView.as_view(
            template_name='autenticacao/alterar_senha.html',
            success_url=reverse_lazy('autenticacao:senha_alterada')  # Redirecionamento após alteração
        ),
        name='alterar_senha'
    ),
    
    # URL após alteração de senha
    path(
        'senha_alterada/',
        PasswordChangeDoneView.as_view(template_name='autenticacao/senha_alterada.html'),
        name='senha_alterada'
    ),
]
