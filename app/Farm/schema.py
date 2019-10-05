from .models import Farm
import graphene
from graphene_django import DjangoObjectType
from County.models import County
from Packages.models import FarmPackage
from Members.models import Member
from Wards.models import Ward
import random

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
        farm.valid = True

        farm.save()

        return CreateFarm(farm=farm)


def getValidAccount():
    while True:
        account = f"FM{random.randint(0,9)}{random.randint(80,999)}{random.randint(50,999)}"
        if not Farm.objects.filter(accounts=account).exists():
            return account


class UpdateFarmAccounts(graphene.Mutation):
    farms = graphene.List(FarmType)

    def mutate(self, info):
        farms = Farm.objects.all()
        
        for farm in farms:
            farm.account = getValidAccount()
            farm.save()

        return UpdateFarmAccounts(farms=farms)

class UpdateFarm(graphene.Mutation):
    farm = graphene.Field(FarmType)

    class Arguments:
        farm_id = graphene.Int(required=True)
        name = graphene.String()
        package_id = graphene.Int()
        package_update_date = graphene.DateTime()

    def mutate(self, info, farm_id, name, package_id, package_update_date):
        farm = Farm.objects.get(id=farm_id)
        package = FarmPackage.objects.get(id=package_id)

        farm.name = name
        farm.package = package
        farm.package_update_date = package_update_date

        farm.save()

        return UpdateFarm(farm=farm)


class Mutation(graphene.ObjectType):
    create_farm = CreateFarm.Field()
    update_farm = UpdateFarm.Field()
