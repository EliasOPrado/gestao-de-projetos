from django.urls import path, include
from rest_framework import routers

from graphene_django.views import GraphQLView
from core.graphql.schema import schema
from django.views.decorators.csrf import csrf_exempt

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
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
