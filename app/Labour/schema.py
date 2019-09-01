from django.db.models import Q
from .models import LabourService
import graphene
from graphene_django import DjangoObjectType


class LabourType(DjangoObjectType):
    class Meta:
        model = LabourService


class Query(graphene.ObjectType):
    LabourServicez = graphene.List(LabourType, name=graphene.String())

    def resolve_LabourServicez(self, info, name=None):
        srv = LabourService.objects.all()
        print(srv)
        if name:
            filters = (
                Q(title__icontains=name)
            )
            srv = srv.filter(filters)

        return srv