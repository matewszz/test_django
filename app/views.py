from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render

from app.models import Municipio
from authentication.models import Crianca, User


@login_required(login_url="/accounts/login/")
def home(request):
    context = {}
    var_adm = False

    if request.user.permissao == "Cliente" and request.user.cpf:
        tds_criancas = Crianca.objects.filter(responsavel=request.user.id).order_by("-nome")
        context["todas_criancas"] = tds_criancas
    else:
        tds_criancas = (
            Crianca.objects
            .select_related("responsavel", "responsavel__municipio")
            .order_by("nome")
        )
        var_adm = True

    municipio_ids = (
        tds_criancas
        .filter(responsavel__isnull=False, responsavel__municipio__isnull=False)
        .values_list("responsavel__municipio_id", flat=True)
        .distinct()
    )

    todos_municipios = (
        Municipio.objects
        .filter(id__in=municipio_ids)
        .order_by("municipio")
    )

    context["adm"] = var_adm
    context["todas_criancas"] = tds_criancas
    context["todos_municipios"] = todos_municipios

    context["adm"] = var_adm
    return render(request, "pages/home.html", context)

def cadastro(request):
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
            municipio=Municipio.objects.get(id=request.POST.get("municipio")),
        )

        Crianca.objects.create(
            nome=request.POST.get("nome_crianca"),
            sobrenome=request.POST.get("sobrenome_crianca"),
            ultima_vacina=var_ultima_vacina,
            proxima_vacina=var_prox_vacina,
            genero=request.POST.get("genero_crianca"),
            responsavel = var_user,
        )

        messages.success(request, "Cadastro realizado com sucesso, Faça login.")

    context = {
        "todas_cidades":  Municipio.objects.all()
    }

    return render(request, "pages/cadastro.html", context)


def dashboard(request):
    if request.user.permissao == "Cliente" and request.user.cpf:
        messages.warning(request, "Você não possui acesso!")
        return redirect("app:home")

    hoje = date.today()

    # ---------- CARD 1 ----------
    total = Crianca.objects.count()

    # ---------- CARD 2 ----------
    em_dia = Crianca.objects.filter(
        Q(proxima_vacina__gt=hoje) | Q(proxima_vacina__isnull=True)
    ).count()
    qtd_ok = (em_dia / total * 100.0) if total else 0.0

    # ---------- CARD 3 ----------
    inicio_mes = hoje.replace(day=1)
    if hoje.month == 12:
        fim_mes = hoje.replace(year=hoje.year + 1, month=1, day=1)
    else:
        fim_mes = hoje.replace(month=hoje.month + 1, day=1)

    total_mes_atual = Crianca.objects.filter(
        proxima_vacina__gte=inicio_mes,
        proxima_vacina__lt=fim_mes
    )
    atrasadas_mes = total_mes_atual.filter(proxima_vacina__lt=hoje).count()
    total_count = total_mes_atual.count()
    atrasadas_total = Crianca.objects.filter(proxima_vacina__lte=hoje).count()

    # ---------- DADOS PARA MAPA ----------
    atrasadas = Crianca.objects.filter(proxima_vacina__lte=hoje)
    municipios_atrasados = (
        atrasadas
        .values(
            "responsavel__municipio__municipio",
            "responsavel__municipio__uf",
            "responsavel__municipio__latitude",
            "responsavel__municipio__longitude"
        )
        .annotate(total=Count("id"))
        .order_by("responsavel__municipio__uf", "responsavel__municipio__municipio")
    )

    localizacao = []
    for m in municipios_atrasados:
        if m["responsavel__municipio__latitude"] and m["responsavel__municipio__longitude"]:
            localizacao.append({
                "municipio": m["responsavel__municipio__municipio"],
                "uf": m["responsavel__municipio__uf"],
                "lat": m["responsavel__municipio__latitude"],
                "lon": m["responsavel__municipio__longitude"],
                "qtd": m["total"],
            })

    # ---------- CONTEXT ----------
    context = {
        "cadastro_total": total,
        "vacinaca_ok": qtd_ok,
        "atrasados_mes": (atrasadas_mes / total_count * 100) if total_count else 0,
        "em_dia": em_dia,
        "atrasadas_total": atrasadas_total,
        "localizacao": localizacao,
    }

    return render(request, "pages/dash.html", context)
