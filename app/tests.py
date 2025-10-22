from django.test import TestCase
from django.urls import resolve, reverse
from app import views



# Teste Urls
class AppURLsTest(TestCase):
    def test_home_url_accesso_correto(self):
        url = reverse("app:home")
        self.assertEqual(url, "/")

    def test_cadastro_url_accesso_correto(self):
        url = reverse("app:cadastro")
        self.assertEqual(url, "/cadastro")

    def test_dashboard_url_accesso_correto(self):
        url = reverse("app:dashboard")
        self.assertEqual(url, "/dashboard")


# acesso na view correta
class AppViewsTest(TestCase):
    def test_view_accesso_correto(self):
        view = resolve(reverse("app:home"))
        self.assertIs(view.func, views.home)

        view = resolve(reverse("app:cadastro"))
        self.assertIs(view.func, views.cadastro)

        view = resolve(reverse("app:dashboard"))
        self.assertIs(view.func, views.dashboard)
