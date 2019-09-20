from django.db.models import Q
from .models import LabourService, PayPeriod, LaboursRequest
import graphene
from graphene_django import DjangoObjectType

class LabourType(DjangoObjectType):
    class Meta:
        model = LabourService

class LabourRequestType(DjangoObjectType):
    class Meta:
        model = LaboursRequest


class Query(graphene.ObjectType):
    services = graphene.List(LabourType, name=graphene.String())
    labourRequests = graphene.List(LabourRequestType, ward=graphene.Int(), service=graphene.Int())

    def resolve_services(self, info, name=None):
        srv = LabourService.objects.all()
        print(srv)
        if name:
            filters = (
                Q(title__icontains=name)
            )
            srv = srv.filter(filters)

        return srv

    def resolve_labourRequests(self, info, ward=None, service=None):
        lrs = LaboursRequest.objects.all()

        return lrs