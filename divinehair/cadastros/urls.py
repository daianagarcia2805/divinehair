from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
    path('agendamentos/', views.lista_agendamentos, name='lista_agendamentos'),
    path('agendamentos/criar/', views.cria_agendamento, name='cria_agendamento'),
    path('agendamentos/editar/<int:pk>/', views.edita_agendamento, name='edita_agendamento'),
    path('agendamentos/deletar/<int:pk>/', views.deleta_agendamento, name='deleta_agendamento'),
]