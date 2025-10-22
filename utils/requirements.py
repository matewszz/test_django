# flake8: noqa
import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


from app.models import Municipio, Vacina

################ popular base de dados com os estado e municipios ##############

ufs = {
    11: "RO", 12: "AC", 13: "AM", 14: "RR", 15: "PA",
    16: "AP", 17: "TO", 21: "MA", 22: "PI", 23: "CE",
    24: "RN", 25: "PB", 26: "PE", 27: "AL", 28: "SE",
    29: "BA", 31: "MG", 32: "ES", 33: "RJ", 35: "SP",
    41: "PR", 42: "SC", 43: "RS", 50: "MS", 51: "MT",
    52: "GO", 53: "DF"
}

def popular_municipios():
    municipalities_url = "utils/municipios.json"

    with open(municipalities_url, "r", encoding="utf-8-sig") as f:
        data = json.load(f)

    municipios_para_criar = []

    for municipio in data:
        try:
            municipio_nome = (municipio.get("nome") or "").strip()
            uf_sigla = ufs.get(municipio.get("codigo_uf"))
            lat = municipio.get("latitude")
            lon = municipio.get("longitude")

            if uf_sigla != "GO":
                continue

            if not Municipio.objects.filter(municipio=municipio_nome, uf=uf_sigla).exists():
                municipios_para_criar.append(Municipio(municipio=municipio_nome, uf=uf_sigla, latitude=lat, longitude=lon))
            else:
                var_mun = Municipio.objects.filter(municipio=municipio_nome, uf=uf_sigla).first()
                var_mun.latitude = lat
                var_mun.longitude = lon
                var_mun.save()

        except Exception as ex:
            print(ex)

    if municipios_para_criar:
        Municipio.objects.bulk_create(municipios_para_criar)

    print("municipios populados com sucesso.")


def populate_vacinas():
    vacinas = [
        {
            "nome": "BCG",
            "idade_recomendada": 0,
            "descricao": "Protege contra as formas graves de tuberculose (miliar e meníngea).",
            "numero_doses": 1,
            "intervalo_doses": "",
            "obrigatoria": True,
        },
        {
            "nome": "Hepatite B",
            "idade_recomendada": 0,
            "descricao": "Previne a hepatite B, doença viral que afeta o fígado.",
            "numero_doses": 3,
            "intervalo_doses": "0, 2 e 6 meses",
            "obrigatoria": True,
        },
        {
            "nome": "Pentavalente",
            "idade_recomendada": 1,
            "descricao": "Combina DTP (tríplice bacteriana), Hib e Hepatite B.",
            "numero_doses": 3,
            "intervalo_doses": "60 dias",
            "obrigatoria": True,
        },
        {
            "nome": "Poliomielite (VIP/VOP)",
            "idade_recomendada": 1,
            "descricao": "Previne a paralisia infantil causada pelo poliovírus.",
            "numero_doses": 5,
            "intervalo_doses": "2 meses",
            "obrigatoria": True,
        },
        {
            "nome": "Rotavírus",
            "idade_recomendada": 2,
            "descricao": "Previne diarreias graves causadas pelo rotavírus.",
            "numero_doses": 2,
            "intervalo_doses": "60 dias",
            "obrigatoria": True,
        },
        {
            "nome": "Pneumocócica 10-valente",
            "idade_recomendada": 4,
            "descricao": "Previne doenças causadas pelo Streptococcus pneumoniae, como meningite e pneumonia.",
            "numero_doses": 3,
            "intervalo_doses": "2 meses",
            "obrigatoria": True,
        },
        {
            "nome": "Meningocócica C",
            "idade_recomendada": 5,
            "descricao": "Previne meningite e infecções graves causadas pela bactéria Neisseria meningitidis tipo C.",
            "numero_doses": 3,
            "intervalo_doses": "60 dias",
            "obrigatoria": True,
        },
        {
            "nome": "Febre Amarela",
            "idade_recomendada": 6,
            "descricao": "Previne a febre amarela, doença viral transmitida por mosquitos.",
            "numero_doses": 2,
            "intervalo_doses": "até 4 anos",
            "obrigatoria": True,
        },
        {
            "nome": "Tríplice Viral (SCR)",
            "idade_recomendada": 5,
            "descricao": "Previne sarampo, caxumba e rubéola.",
            "numero_doses": 2,
            "intervalo_doses": "3 meses",
            "obrigatoria": True,
        },
        {
            "nome": "Varicela",
            "idade_recomendada": 7,
            "descricao": "Previne a catapora (varicela).",
            "numero_doses": 1,
            "intervalo_doses": "",
            "obrigatoria": True,
        },
    ]

    criados = 0
    for v in vacinas:
        obj, criados_flag = Vacina.objects.get_or_create(
            nome=v["nome"],
            defaults=v,
        )
        if criados_flag:
            criados += 1

    print(f"{criados} vacinas criadas com sucesso!")

if __name__ == "__main__":
    popular_municipios()
    populate_vacinas()

