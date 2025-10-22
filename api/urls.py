from rest_framework.routers import SimpleRouter

from api.views import CriancaViewSet

####################    API     ####################

router = SimpleRouter()

# User
router.register("criancas", CriancaViewSet)

