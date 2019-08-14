from .models import Country
import graphene
from graphene_django import DjangoObjectType


class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class Query(graphene.ObjectType):
    countries = graphene.List(CountryType)

    def resolve_countries(self, info):
        return Country.objects.all()
