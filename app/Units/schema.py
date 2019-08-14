from .models import Unit
import graphene
from graphene_django import DjangoObjectType


class UnitType(DjangoObjectType):
    class Meta:
        model = Unit


class Query(graphene.ObjectType):
    units = graphene.List(UnitType)

    def resolve_units(self, info):
        return Unit.objects.all()
