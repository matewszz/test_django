# flake8: noqa

import os
import random
import sys
from datetime import date, timedelta

from faker import Faker

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from app.models import Municipio
from authentication.models import Crianca, User

fake = Faker("pt_BR")


def user_fake(n=15):
    municipios = list(Municipio.objects.all())

    genero_choices = ["Masculino", "Feminino"]
    users = []
    criancas = []

    for i in range(n):
        # ---------- Usuário ----------
        nome = fake.first_name()
        sobrenome = fake.last_name()
        username = f"{nome.lower()}.{sobrenome.lower()}{i}"
        municipio = random.choice(municipios)

        user = User.objects.create_user(
            username=username,
            email=fake.email(),
            password="123456",
            first_name=nome,
            last_name=sobrenome,
            telefone=fake.phone_number(),
            cpf=fake.cpf(),
            municipio=municipio,
            permissao="Cliente",
            status="Ativo",
        )
        users.append(user)

        # ---------- Criança ----------
        nome_c = fake.first_name()
        sobrenome_c = fake.last_name()
        genero = random.choice(genero_choices)
        hoje = date.today()
        ultima_vacina = hoje - timedelta(days=random.randint(30, 400))
        proxima_vacina = ultima_vacina + timedelta(days=random.randint(90, 365))

        crianca = Crianca.objects.create(
            nome=nome_c,
            sobrenome=sobrenome_c,
            genero=genero,
            ultima_vacina=ultima_vacina,
            proxima_vacina=proxima_vacina,
            responsavel=user,
        )
        criancas.append(crianca)

    print("Usuários criados com sucesso!")


if __name__ == "__main__":
    user_fake()
