from County.models import County
from Buyer.models import Buyer
from Products.models import Product
from Units.models import Unit
from Farm.models import Farm

from .models import Tender, Bid
import graphene
from graphene_django import DjangoObjectType


class TenderType(DjangoObjectType):
    class Meta:
        model = Tender


class BidType(DjangoObjectType):
    class Meta:
        model = Bid


class Query(graphene.ObjectType):
    bids = graphene.List(BidType)
    tenders = graphene.List(TenderType)

    def resolve_tenders(self, info):
        return Tender.objects.all()

    def resolve_bids(self, info):
        return Bid.objects.all()


class CreateTender(graphene.Mutation):
    tender = graphene.Field(TenderType)

    class Arguments:
        buyer_id = graphene.Int(required=True)
        product_id = graphene.Int(required=True)
        county_id = graphene.Int(required=True)
        amount = graphene.Int()
        unit_id = graphene.Int(required=True)

    def mutate(self, buyer_id, product_id, county_id, amount, unit_id):
        tender = Tender(amount=amount)
        buyer = Buyer.objects.get(id=buyer_id)
        product = Product.objects.get(id=product_id)
        county = County.objects.get(id=county_id)
        unit = County.objects.get(id=unit_id)
        tender.buyer = buyer
        tender.product = product
        tender.county = county
        tender.unit = unit

        tender.save()

        return CreateTender(tender=tender)


class UpdateTender(graphene.Mutation):
    tender = graphene.Field(TenderType)

    class Arguments:
        tender_id = graphene.Int(required=True)

        amount = graphene.Int()
        unit_id = graphene.Int()

    def mutate(self, tender_id, amount, unit_id):
        tender = Tender.objects.get(id=tender_id)
        unit = Unit.objects.get(id=unit_id)
        tender.amount = amount
        tender.unit = unit

        tender.save()

        return UpdateTender(tender=tender)


class Mutation(graphene.ObjectType):
    create_tender = CreateTender.Field()
    update_tender = UpdateTender.Field()
