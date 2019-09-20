import datetime

from django.db.models import Q
from Wards.models import Ward
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
        lrs = LaboursRequest.objects.filter(startDate__gt=datetime.datetime.now())
        if ward:
            w = Ward.objects.get(id=ward)
            lrs = LaboursRequest.objects.filter(ward=w)
        if service:
            s = LabourService.objects.get(id=service)
            lrs = LaboursRequest.objects.filter(service=s)

        if ward and service:
            w = Ward.objects.get(id=ward)
            s = LabourService.objects.get(id=service)
            lrs = LaboursRequest.objects.filter(service=s).filter(ward=w)

        return lrs
