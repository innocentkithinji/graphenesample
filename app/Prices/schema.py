from django.db.models import Q
from .models import Prices
import graphene
from graphene_django import DjangoObjectType


class PricesType(DjangoObjectType):
    class Meta:
        model = Prices


class Query(graphene.ObjectType):
    prices = graphene.List(PricesType, countyID=graphene.Int(), productID=graphene.Int())

    def resolve_prices(self, info, countyID=None, productID=None):
        prices = Prices.objects.all()

        return prices
