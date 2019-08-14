from .models import BuyerPackage, FarmPackage
import graphene
from graphene_django import DjangoObjectType


class BuyerPackageType(DjangoObjectType):
    class Meta:
        model = BuyerPackage


class FarmPackageType(DjangoObjectType):
    class Meta:
        model = FarmPackage


class Query(graphene.ObjectType):
    buyerPackages = graphene.List(BuyerPackageType)
    farmPackages = graphene.List(FarmPackageType)

    def resolve_buyerPackages(self, info):
        return BuyerPackage.objects.all()

    def resolve_buyerPackages(self, info):
            return FarmPackage.objects.all()


