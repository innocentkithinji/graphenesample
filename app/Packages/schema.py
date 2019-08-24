from .models import BuyerPackage, FarmPackage, Period
import graphene
from graphene_django import DjangoObjectType


class BuyerPackageType(DjangoObjectType):
    class Meta:
        model = BuyerPackage


class FarmPackageType(DjangoObjectType):
    class Meta:
        model = FarmPackage


class PeriodType(DjangoObjectType):
    class Meta:
        model = Period
        only_fields = ('id', 'name', 'number_of_days')


class Query(graphene.ObjectType):
    buyerPackages = graphene.List(BuyerPackageType)
    farmPackages = graphene.List(FarmPackageType)
    period = graphene.Field(PeriodType)

    def resolve_buyerPackages(self, info):
        return BuyerPackage.objects.all()

    def resolve_farmPackages(self, info):
        return FarmPackage.objects.all()

    def resolve_period(self, info):
        return Period.objects.all()
