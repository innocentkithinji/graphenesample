from .models import Category
import graphene
from graphene_django import DjangoObjectType


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info):
        return Category.objects.all()
