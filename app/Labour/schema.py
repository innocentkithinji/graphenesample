import datetime

from django.db.models import Q
from Wards.models import Ward

from Buyer.models import Buyer
from Farm.models import Farm
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


class createLabourReq(graphene.Mutation):
    request = graphene.Field(LabourRequestType)

    class Arguments:
        ward = graphene.Int(required=True)
        farm = graphene.Int(required=False)
        buyer = graphene.Int(required=False)
        service = graphene.Int(required=True)
        startDate = graphene.String(required=True)
        time = graphene.String(required=True)
        payPeriod = graphene.Int(required=True)
        pay = graphene.Int(required=True)
        periodLength = graphene.Int(required=True)

    def mutate(self, info, ward, farm, buyer, service, startDate, time, payPeriod, pay, periodLength):
        request = LaboursRequest()
        w = Ward.objects.get(id=ward)
        if farm:
            f = Farm.objects.get(id=farm)
            request.farm = f
        else:
            b = Buyer.objects.get(id=buyer)
            request.buyer = b
        s = LabourService.objects.get(id=service)
        date_time = f"{startDate} {time}"
        start_date_time = datetime.datetime.strptime(date_time, '%d-%m-%Y %H:%M')
        request.ward = w
        request.service = s
        request.payPeriod = PayPeriod.objects.get(id=payPeriod)
        request.pay = pay
        request.periodNumber = periodLength
        request.startDate = start_date_time

        request.save()

        return createLabourReq(request=request)


class Mutation(graphene.ObjectType):
    create_Labour_Req = createLabourReq.Field()