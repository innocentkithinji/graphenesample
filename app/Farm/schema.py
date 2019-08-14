from .models import Farm
import graphene
from graphene_django import DjangoObjectType
from County.models import County
from Packages.models import FarmPackage
from Members.models import Member


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
        latitude = graphene.Float(required=True)
        longitude = graphene.Float(required=True)
        package_id = graphene.Int(required=True)
        owner_id = graphene.Int(required=True)

    def mutate(self, info, county_id, name, latitude, longitude, package_id, owner_id):
        farm = Farm(name=name, latitude=latitude, longitude=longitude)

        county = County.objects.get(id=county_id)
        package = FarmPackage.objects.get(id=package_id)
        owner = Member.objects.get(id=owner_id)

        farm.county = county
        farm.package = package
        farm.owner = owner
        farm.valid = True

        farm.save()

        return CreateFarm(farm=farm)


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