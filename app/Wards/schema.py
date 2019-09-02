from django.db.models import Q
from .models import Ward
import graphene
from graphene_django import DjangoObjectType


class WardType(DjangoObjectType):
    class Meta:
        model = Ward


class Query(graphene.ObjectType):
    wards = graphene.List(WardType, name=graphene.String())

    def resolve_wards(self, info, name=None):
        srv = Ward.objects.all()
        print(srv)
        if name:
            filters = (
                Q(name__icontains=name)
            )
            srv = srv.filter(filters)

        return srv