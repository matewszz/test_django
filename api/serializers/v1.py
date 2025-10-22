from rest_framework import serializers


from authentication.models import Crianca, User


class UserCodeLookupSerializer(serializers.ModelSerializer):
    municipio_nome = serializers.CharField(source="municipio.municipio", read_only=True)

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "municipio_nome"]


class CriancaSerializer(serializers.ModelSerializer):
    responsavel = UserCodeLookupSerializer(read_only=True)
    responsavel_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="responsavel",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Crianca
        fields = [
            "id", "nome", "sobrenome",
            "ultima_vacina", "proxima_vacina", "genero",
            "responsavel",
            "responsavel_id",
        ]
