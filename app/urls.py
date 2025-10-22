from django.urls import path

from . import views

# flake8: noqa
app_name = 'app'

urlpatterns = [
     path('', views.home, name="home"),
     path('administracao', views.admin_page, name="admin_page"),
     path('cadastro', views.cadastro, name="cadastro"),
     ]