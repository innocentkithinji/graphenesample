from .models import County
import graphene
from graphene_django import DjangoObjectType


class CountyType(DjangoObjectType):
    class Meta:
        model = County


class Query(graphene.ObjectType):
    counties = graphene.List(CountyType)

    def resolve_counties(self, info):
        return County.objects.all()
