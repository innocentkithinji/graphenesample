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
