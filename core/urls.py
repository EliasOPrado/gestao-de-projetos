from django.urls import path, include
from rest_framework import routers

from core.api.viewsets import ClienteModelViewSet
from core.api.viewsets import ProjetoModelViewSet
from core.api.viewsets import AtividadeModelViewSet

app_name = "core"

router = routers.DefaultRouter()
router.register(r"clientes", ClienteModelViewSet, basename="clientes")
router.register(r"projetos", ProjetoModelViewSet, basename="projetos")
router.register(r"atividades", AtividadeModelViewSet, basename="atividades")

urlpatterns = [
    path("", include(router.urls)),
]
