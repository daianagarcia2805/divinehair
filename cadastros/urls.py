from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
    path('agendamentos/', views.lista_agendamentos, name='lista_agendamentos'),
    path('agendamentos/criar/', views.cria_agendamento, name='cria_agendamento'),
    path('agendamentos/editar/<int:pk>/', views.edita_agendamento, name='edita_agendamento'),
    path('agendamentos/deletar/<int:pk>/', views.deleta_agendamento, name='deleta_agendamento'),
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/criar/', views.criar_servico, name='criar_servico'),
    path('servicos/editar/<int:pk>/', views.editar_servico, name='editar_servico'),
    path('servicos/deletar/<int:pk>/', views.deletar_servico, name='deletar_servico'),
]