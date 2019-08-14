from .models import Buyer
import graphene
from graphene_django import DjangoObjectType
from County.models import County
from Packages.models import BuyerPackage
from Members.models import Member


class BuyerType(DjangoObjectType):
    class Meta:
        model = Buyer


class Query(graphene.ObjectType):
    buyers = graphene.List(BuyerType)

    def resolve_buyers(self, info):
        return Buyer.objects.all()


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
        buyer.package = package

        buyer.save()

        return CreateBuyer(buyer=buyer)


class UpdateBuyer(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    class Arguments:
        buyer_id = graphene.Int(required=True)
        name = graphene.String()
        county_id = graphene.Int()
        package_id = graphene.Int()
        latitude = graphene.Float()
        longitude = graphene.Float()
        package_update_date = graphene.DateTime()

    def mutate(self, info, buyer_id, name, county_id, latitude, longitude, package_id, package_update_date):
        buyer = Buyer.objects.get(id=buyer_id)
        package = BuyerPackage.objects.get(id=package_id)
        county = County.objects.get(id=county_id)

        buyer.name = name
        buyer.package = package
        buyer.package_update_date = package_update_date
        buyer.county = county
        buyer.longitude = longitude
        buyer.latitude = latitude
        buyer.save()

        return UpdateBuyer(buyer=buyer)


class Mutation(graphene.ObjectType):
    create_buyer = CreateBuyer.Field()
    update_buyer = UpdateBuyer.Field()