import random

import graphene
from County.models import County
from Members.models import Member
from Packages.models import FarmPackage
from Wards.models import Ward
from graphene_django import DjangoObjectType

from datetime import datetime

from .models import Farm


class FarmType(DjangoObjectType):
    class Meta:
        model = Farm


class Query(graphene.ObjectType):
    farms = graphene.List(FarmType)

    def resolve_farms(self, info):
        return Farm.objects.all()


class CreateFarm(graphene.Mutation):
    farm = graphene.Field(FarmType)

    class Arguments:
        name = graphene.String(required=True)
        county_id = graphene.Int(required=True)
        package_id = graphene.Int(required=True)
        owner_id = graphene.Int(required=True)
        ward_id = graphene.Int(required=True)

    def mutate(self, info, county_id, name, ward_id, package_id, owner_id):
        farm = Farm(name=name)

        county = County.objects.get(id=county_id)
        package = FarmPackage.objects.get(id=package_id)
        owner = Member.objects.get(id=owner_id)
        ward = Ward.objects.get(id=ward_id)

        farm.county = county
        farm.package = package
        farm.owner = owner
        farm.Ward = ward
        farm.account = getValidAccount()

        farm.save()

        return CreateFarm(farm=farm)


def getValidAccount():
    while True:
        account = f"FM{random.randint(0, 9)}{random.randint(80, 999)}{random.randint(50, 999)}"
        if not Farm.objects.filter(account=account).exists():
            return account


class UpdateFarmAccounts(graphene.Mutation):
    farms = graphene.Field(FarmType)

    def mutate(self, info):
        farms = Farm.objects.all()
        theFarm = None;
        for farm in farms:
            f = Farm.objects.get(id=farm.id)
            updateAccount = getValidAccount()
            f.accounts = updateAccount
            f.save()
            theFarm = f

        return UpdateFarmAccounts(farms=theFarm)


class UpdateFarm(graphene.Mutation):
    farm = graphene.Field(FarmType)

    class Arguments:
        farm_id = graphene.Int(required=True)
        name = graphene.String()
        package_id = graphene.Int()

    def mutate(self, info, farm_id, name, package_id):
        farm = Farm.objects.get(id=farm_id)
        package = FarmPackage.objects.get(id=package_id)
        farm.name = name
        farm.package = package
        farm.package_update_date = datetime.now()

        farm.save()

        return UpdateFarm(farm=farm)


class Mutation(graphene.ObjectType):
    create_farm = CreateFarm.Field()
    update_farm = UpdateFarm.Field()
    give_farm_accounts = UpdateFarmAccounts.Field()
