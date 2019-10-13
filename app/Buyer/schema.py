import datetime
import random

import graphene
from County.models import County
from Members.models import Member
from Packages.models import BuyerPackage
from graphene_django import DjangoObjectType

from .models import Buyer


class BuyerType(DjangoObjectType):
    class Meta:
        model = Buyer


class Query(graphene.ObjectType):
    buyers = graphene.List(BuyerType)

    def resolve_buyers(self, info):
        return Buyer.objects.all()


def getValidAccount():
    while True:
        account = f"BY{random.randint(0, 9)}{random.randint(111, 999)}{random.randint(222, 999)}"
        if not Buyer.objects.filter(account=account).exists():
            return account


class UpdateBuyerAccounts(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    def mutate(self, info):
        buyers = Buyer.objects.all()
        theBuyer = None
        for buyer in buyers:
            b = Buyer.objects.get(id=buyer.id)
            updateAccount = getValidAccount()
            b.account = updateAccount
            b.save()
            theBuyer = b

        return UpdateBuyerAccounts(buyer=theBuyer)


class CreateBuyer(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    class Arguments:
        name = graphene.String(required=True)
        county_id = graphene.Int(required=True)
        latitude = graphene.Float(required=True)
        longitude = graphene.Float(required=True)
        package_id = graphene.Int(required=True)
        owner_id = graphene.Int(required=True)

    def mutate(self, info, name, county_id, latitude, longitude, package_id, owner_id):
        owner = Member.objects.get(id=owner_id)
        county = County.objects.get(id=county_id)
        package = BuyerPackage.objects.get(id=package_id)

        buyer = Buyer(name=name, latitude=latitude, longitude=longitude)
        buyer.owner = owner
        buyer.county = county
        if package_id == 1:
            buyer.active = True
        buyer.package = package
        buyer.account = getValidAccount()

        buyer.save()

        return CreateBuyer(buyer=buyer)


class UpdateBuyer(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    class Arguments:
        buyer_id = graphene.Int(required=True)
        name = graphene.String()
        package_id = graphene.Int()

    def mutate(self, info, buyer_id, package_id, name=None):
        buyer = Buyer.objects.get(id=buyer_id)
        package = BuyerPackage.objects.get(id=package_id)

        if name:
            buyer.name = name
        buyer.package = package
        buyer.package_update_date = datetime.datetime.now()
        buyer.active = False
        buyer.save()

        return UpdateBuyer(buyer=buyer)


class Mutation(graphene.ObjectType):
    create_buyer = CreateBuyer.Field()
    update_buyer = UpdateBuyer.Field()
    give_buyers_accounts = UpdateBuyerAccounts.Field()
