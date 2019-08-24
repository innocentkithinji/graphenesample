from django.db.models import Q

from .models import Product
import graphene
from graphene_django import DjangoObjectType


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class Query(graphene.ObjectType):
    products = graphene.List(
        ProductType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_products(self, info, search=None, first=None, skip=None, **kwargs):
        rs = Product.objects.all()

        if search:
            filters = (
                    Q(name__icontains=search) |
                    Q(alternative_name__icontains=search)
            )

            rs = rs.filter(filters)
        if skip:
            rs = rs[skip:]
        if first:
            rs = rs[:first]
        return rs
