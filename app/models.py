from django.db import models
from authentication.models import User

STATUS_CHOICE = (
    ("active", "active"),
    ("finished", "finished"),
)


class Base(models.Model):
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class Vacina(Base):
    nome = models.CharField("Nome da vacina", max_length=100)
    idade_recomendada = models.PositiveIntegerField(
        "Idade recomendada", 
        help_text="Ex: 2 meses, 1 ano, 4 anos, reforço aos 5 anos"
    )
    descricao = models.TextField(
        "Descrição", 
        blank=True, 
        help_text="Informações adicionais sobre a vacina, eficácia, doses, etc."
    )
    numero_doses = models.PositiveIntegerField(
        "Número de doses", 
        default=1, 
        help_text="Quantidade total de doses necessárias"
    )
    intervalo_doses = models.CharField(
        "Intervalo entre doses", 
        max_length=50, 
        blank=True, 
        help_text="Ex: 30 dias, 6 meses, anual"
    )
    obrigatoria = models.BooleanField(
        "Obrigatória pelo SUS", 
        default=True
    )
    data_criacao = models.DateTimeField("Data de cadastro", auto_now_add=True)
    data_atualizacao = models.DateTimeField("Última atualização", auto_now=True)

    class Meta:
        verbose_name = "Vacina"
        verbose_name_plural = "Vacinas"
        ordering = ["idade_recomendada", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.idade_recomendada})"


class Municipio(models.Model):
    municipio = models.CharField(max_length=100, default="")
    uf = models.CharField(max_length=2, blank=True, default="")
    latitude = models.FloatField(null=True, blank=True)  
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = "municipio"
        ordering = ["uf", "municipio"]

    def __str__(self):
        return f"{self.municipio} ({self.uf})"