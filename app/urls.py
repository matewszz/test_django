from django.urls import path

from . import views

# flake8: noqa
app_name = 'app'

urlpatterns = [
     path('', views.home, name="home"),
     path('cadastro', views.cadastro, name="cadastro"),
     path('dashboard', views.dashboard, name="dashboard"),

     ]