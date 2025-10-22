from django.urls import path

from . import views

# flake8: noqa
app_name = 'authentication'

urlpatterns = [
    path("login/", views.login_view, name="account_login"),
    path("logout/", views.logout_view, name="account_logout"),
    ]