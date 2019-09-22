from .models import Labourer
import graphene
from graphene_django import DjangoObjectType


class LabourerType(DjangoObjectType):
    class Meta:
        model = Labourer


class Query(graphene.ObjectType):
    labourers = graphene.List(LabourerType)

    def resolve_labourers(self, info):
        return Labourer.objects.all()
