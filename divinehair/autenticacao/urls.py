from . import views
from django.urls import path
from .views import login_view
from .views import logout_view
from .views import admin_dashboard
from .views import funcionario_dashboard
from .views import cliente_dashboard




app_name = "autenticacao"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('funcionario/dashboard/', views.funcionario_dashboard, name='funcionario_dashboard'),
    path('cliente/dashboard/', views.cliente_dashboard, name='cliente_dashboard'),
]