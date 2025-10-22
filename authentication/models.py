from django.db import models
from django.contrib.auth.models import AbstractUser

PERMISSAO_CHOICES = [
    ("Cliente", "Cliente"),
    ("Administrador", "Administrador"),
]

GENERO_CHOICE = (
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino'),
)

STATUS_CHOICES = [("Ativo", "Ativo"), ("Finalizado", "Finalizado")]

class User(AbstractUser):
    telefone = models.CharField(max_length=50, blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modificado_em = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default="Ativo")
    permissao = models.CharField(max_length=50, default="Cliente", null=True, choices=PERMISSAO_CHOICES)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    municipio = models.ForeignKey("app.Municipio", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "usuario"
        verbose_name_plural = "usuario"


class Crianca(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    ultima_vacina = models.DateField(blank=True, null=True)
    proxima_vacina = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=100, null=True, blank=True, choices=GENERO_CHOICE)
    responsavel = models.ForeignKey("authentication.User", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "crianca"
        verbose_name_plural = "crianca"