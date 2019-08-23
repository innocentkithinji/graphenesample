from django.db.models import Q

from .models import Category
import graphene
from graphene_django import DjangoObjectType


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    categories = graphene.List(
        CategoryType,
        search=graphene.String(),
        first=graphene.Int(),
        skip=graphene.Int()
    )

    def resolve_categories(self, info, search=None,first=None, skip=None, **kwargs):
        rs = Category.objects.all()

        if search:
            filters = (
                    Q(name__icontains=search) |
                    Q(alternative_name__icontains=search) |
                    Q(description__icontains=search)
            )

            rs = rs.filter(filters)
        if skip:
            rs = rs[skip:]
        if first:
            rs = rs[:first]

        return rs
