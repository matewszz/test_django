from datetime import date

from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import CriancaSerializer
from authentication.models import Crianca


class CriancaViewSet(viewsets.ModelViewSet):
    queryset = Crianca.objects.select_related("responsavel__municipio").all()
    serializer_class = CriancaSerializer
    http_method_names = ["get", "post", "put", "patch", "head", "options"]

    @action(detail=False, methods=["get"], url_path=r"municipio/(?P<municipio>[^/]+)")
    def por_municipio(self, request, municipio=None):
        try:
            qs = self.queryset.filter(
                responsavel__municipio__municipio__iexact=municipio
            )
            if not qs.exists():
                return Response(
                    {"detail": f"Nenhuma criança encontrada em {municipio}."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"detail": str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    # /criancas/em-dia/?municipio=Anápolis&mes=10&ano=2025
    @action(detail=False, methods=["get"], url_path=r"em-dia")
    def em_dia(self, request):
        hoje = date.today()
        municipio = request.query_params.get("municipio")
        mes = request.query_params.get("mes")
        ano = request.query_params.get("ano")

        qs = self.queryset.filter(
            Q(proxima_vacina__gt=hoje) | Q(proxima_vacina__isnull=True)
        )

        if municipio:
            qs = qs.filter(responsavel__municipio__municipio__iexact=municipio)

        if mes and ano:
            qs = qs.filter(proxima_vacina__month=int(mes), proxima_vacina__year=int(ano))

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # /criancas/atrasadas/?municipio=Anápolis&mes=10&ano=2025
    @action(detail=False, methods=["get"], url_path=r"atrasadas")
    def atrasadas(self, request):
        hoje = date.today()
        municipio = request.query_params.get("municipio")
        mes = request.query_params.get("mes")
        ano = request.query_params.get("ano")

        qs = self.queryset.filter(proxima_vacina__isnull=False, proxima_vacina__lte=hoje)

        if municipio:
            qs = qs.filter(responsavel__municipio__municipio__iexact=municipio)

        if mes and ano:
            qs = qs.filter(proxima_vacina__month=int(mes), proxima_vacina__year=int(ano))

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
