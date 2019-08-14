from .models import Product
import graphene
from graphene_django import DjangoObjectType


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    products = graphene.List(ProductType)

    def resolve_products(self, info):
        return Product.objects.all()
