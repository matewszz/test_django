from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.models import Crianca
from app.models import Municipio

User = get_user_model()

@override_settings(REST_FRAMEWORK={"DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"]})
class CriancaTests(APITestCase):
    def setUp(self):
        # auth
        self.user = User.objects.create_user(username="u", password="p")
        self.client.force_authenticate(user=self.user)

        # municipios
        self.m_goiania = Municipio.objects.create(municipio="Goiânia", uf="GO", latitude=-16.6864, longitude=-49.2643)
        self.m_anapolis = Municipio.objects.create(municipio="Anápolis", uf="GO", latitude=-16.3281, longitude=-48.9530)

        # responsáveis
        self.resp_gyn = User.objects.create_user(username="r1", password="x", first_name="Ana", municipio=self.m_goiania)
        self.resp_ana = User.objects.create_user(username="r2", password="x", first_name="Beto", municipio=self.m_anapolis)

        # datas
        self.hoje = date.today()
        self.passado = self.hoje - timedelta(days=5)
        self.hoje_mesmo = self.hoje
        self.futuro_curto = self.hoje + timedelta(days=3)
        self.futuro_longo = self.hoje + timedelta(days=10)

        # Goiânia
        self.c_future_gyn = Crianca.objects.create(nome="FutGyn", sobrenome="A", responsavel=self.resp_gyn, proxima_vacina=self.futuro_longo)
        self.c_null_gyn   = Crianca.objects.create(nome="NullGyn", sobrenome="B", responsavel=self.resp_gyn, proxima_vacina=None)
        self.c_past_gyn   = Crianca.objects.create(nome="PastGyn", sobrenome="C", responsavel=self.resp_gyn, proxima_vacina=self.passado)
        self.c_today_gyn  = Crianca.objects.create(nome="TodayGyn", sobrenome="D", responsavel=self.resp_gyn, proxima_vacina=self.hoje_mesmo)

        # Anápolis
        self.c_future_ana = Crianca.objects.create(nome="FutAna", sobrenome="E", responsavel=self.resp_ana, proxima_vacina=self.futuro_curto)
        self.c_past_ana   = Crianca.objects.create(nome="PastAna", sobrenome="F", responsavel=self.resp_ana, proxima_vacina=self.hoje - timedelta(days=1))

    # ---------- LIST ----------
    def test_todas_criancas(self):
        resp = self.client.get("/api/v1/criancas/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # ---------- POR MUNICIPIO ----------
    def test_por_municipio_goiania(self):
        resp = self.client.get("/api/v1/criancas/municipio/Goiânia/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        self.assertTrue({"FutGyn", "NullGyn", "PastGyn", "TodayGyn"}.issubset(nomes))
        # não deve incluir crianças de Anápolis
        self.assertNotIn("FutAna", nomes)
        self.assertNotIn("PastAna", nomes)

    def test_por_municipio_inexistente_404(self):
        resp = self.client.get("/api/v1/criancas/municipio/CidadeQueNaoExiste/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ---------- EM DIA ----------
    def test_em_dia_sem_filtro(self):
        resp = self.client.get("/api/v1/criancas/em-dia/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        # inclui futures e null
        self.assertIn("FutGyn", nomes)
        self.assertIn("NullGyn", nomes)
        self.assertIn("FutAna", nomes)
        # exclui passado e hoje
        self.assertNotIn("PastGyn", nomes)
        self.assertNotIn("PastAna", nomes)
        self.assertNotIn("TodayGyn", nomes)

    def test_em_dia_filtrado_por_municipio(self):
        resp = self.client.get("/api/v1/criancas/em-dia/?municipio=Goiânia")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        self.assertIn("FutGyn", nomes)
        self.assertIn("NullGyn", nomes)
        self.assertNotIn("FutAna", nomes)   # outra cidade

    def test_em_dia_filtrado_por_mes_ano(self):
        mes = self.futuro_curto.month
        ano = self.futuro_curto.year
        resp = self.client.get(f"/api/v1/criancas/em-dia/?mes={mes}&ano={ano}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        self.assertIn("FutAna", nomes)
        self.assertNotIn("NullGyn", nomes)

    # ---------- ATRASADAS ----------
    def test_atrasadas_sem_filtro(self):
        resp = self.client.get("/api/v1/criancas/atrasadas/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        self.assertIn("PastGyn", nomes)
        self.assertIn("PastAna", nomes)

        # hoje conta como atrasada (<= hoje)
        self.assertIn("TodayGyn", nomes)
        self.assertNotIn("NullGyn", nomes)
        self.assertNotIn("FutGyn", nomes)
        self.assertNotIn("FutAna", nomes)

    def test_atrasadas_filtrado_por_municipio(self):
        resp = self.client.get("/api/v1/criancas/atrasadas/?municipio=Anápolis")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        self.assertIn("PastAna", nomes)
        # não deve trazer atrasadas de Goiânia
        self.assertNotIn("PastGyn", nomes)
        self.assertNotIn("TodayGyn", nomes)

    def test_atrasadas_filtrado_por_mes_ano(self):
        mes = self.passado.month
        ano = self.passado.year
        resp = self.client.get(f"/api/v1/criancas/atrasadas/?mes={mes}&ano={ano}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        nomes = {c["nome"] for c in resp.data}
        self.assertIn("PastGyn", nomes)
        self.assertNotIn("NullGyn", nomes)  # sem data nunca entra
