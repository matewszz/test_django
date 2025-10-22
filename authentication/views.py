from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate

from .forms import *

def login_view(request):
    context = {}

    form_login = LoginForm()

    if request.POST:

        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            authenticated_user = authenticate(request, username=username, password=password)

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('/')
            else:
                context['msg'] = "Credenciais inválidas!"
        else:
            context['msg'] = "Credenciais inválidas!"

    context['form_login'] = form_login
    return render(request, "pages/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("authentication:account_login")