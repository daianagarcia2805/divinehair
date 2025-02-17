from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.deletion import ProtectedError
import datetime # * trabalhar com datas e horas em Python


# Tabela de Perfis de Usuários (Admin, Funcionário, Cliente)
class Perfil(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def delete(self, *args, **kwargs):
        if self.usuario_set.exists():
            raise ProtectedError(
                "Não é possível excluir este perfil, pois ele possui usuários vinculados.",
                self
            )
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.nome


# Tabela de Usuários (clientes, funcionários, administradores)
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nome, password=None):
        if not email:
            raise ValueError('O usuário deve ter um endereço de e-mail')
        user = self.model(email=self.normalize_email(email), nome=nome)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, password=None):
        user = self.create_user(email, nome, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    nome = models.CharField(max_length=300)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    perfis = models.ManyToManyField(Perfil)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def tem_perfil(self, perfil_nome):
        return self.perfis.filter(nome=perfil_nome).exists()


# Tabela de Serviços oferecidos no salão de beleza
class Servico(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.nome


# Tabela de Agendamentos
class Agendamento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=100, choices=[('agendado', 'Agendado'), ('realizado', 'Realizado'), ('cancelado', 'Cancelado')], default='agendado')

    def __str__(self):
        return f"{self.usuario.nome} - {self.servico.nome} - {self.data_hora}"


# Tabela de Log de Acesso (para auditoria e controle de segurança)
class LogAcesso(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    acao = models.CharField(max_length=100, choices=[('login', 'Login'), ('logout', 'Logout'), ('alteracao_senha', 'Alteração de senha')])

    def __str__(self):
        return f"{self.usuario.nome} - {self.acao} - {self.data_hora}"


# Tabela de Alteração de Senha
class AlteracaoSenha(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nova_senha = models.CharField(max_length=200)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.nome} - Alteração de senha em {self.data_hora}"
