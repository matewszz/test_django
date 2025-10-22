from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from app.forms import *
from authentication.models import Crianca, User


@login_required(login_url="/login/")
def home(request):
    context = {}

    if request.user.permissao == "Administrador":
        context["todas_criancas"] = Crianca.objects.all().order_by("-nome")
    else:
        context["todas_criancas"] = Crianca.objects.filter(id=request.user.responsavel).order_by("-nome")


    return render(request, "pages/home.html", context)


@login_required(login_url="/login/")
def admin_page(request):
    if not hasattr(request.user, "rule") or request.user.rule != "Administrador":
        raise Http404("Acesso negado")
    
    context = {}

    return render(request, "pages/admin-page.html", context)


def cadastro(request):
    context = {}

    if request.POST:
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            messages.warning(request, "Este e-mail já está cadastrado, Faça login.")
            return redirect("app:cadastro")

        if request.POST.get("ultima_vacina"):
            var_ultima_vacina = request.POST.get("ultima_vacina")
        else:
            var_ultima_vacina = None

        if request.POST.get("ultima_vacina"):
            var_prox_vacina = request.POST.get("proxima_vacina")
        else:
            var_prox_vacina = None

        var_user = User.objects.create_user(
            username=email,
            email=email,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            telefone=request.POST.get("telefone"),
            password=request.POST.get("password"),
            cpf=request.POST.get("cpf"),
        )

        Crianca.objects.create(
            nome=request.POST.get("nome_crianca"),
            sobrenome=request.POST.get("sobrenome_crianca"),
            ultima_vacina=var_ultima_vacina,
            proxima_vacina=var_prox_vacina,
            genero=request.POST.get("genero_crianca"),
            responsavel = User.objects.get(id=var_user.id),
        )

        messages.success(request, "Cadastro realizado com sucesso, Faça login.")

    return render(request, "pages/cadastro.html", context)