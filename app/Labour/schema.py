from django.db.models import Q
from .models import LabourService
import graphene
from graphene_django import DjangoObjectType


class LabourType(DjangoObjectType):
    class Meta:
        model = LabourService


class Query(graphene.ObjectType):
    services = graphene.List(LabourType, name=graphene.String())

    def resolve_services(self, name=None):
        srv = LabourService.objects.all()

        if name:
            filters = (
                Q(title_icontains=name)
            )
            srv = srv.filter(filters)

        return srv