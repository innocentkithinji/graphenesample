from django.db.models import Q
from .models import LabourServices
import graphene
from graphene_django import DjangoObjectType


class LabourType(DjangoObjectType):
    class Meta:
        model = LabourServices


class Query(graphene.ObjectType):
    LabourServicez = graphene.List(LabourType, name=graphene.String())

    def resolve_LabourServicez(self, name=None):
        srv = LabourServices.objects.all()
        print(srv)
        if name:
            filters = (
                Q(title__icontains=name)
            )
            srv = srv.filter(filters)

        return srv