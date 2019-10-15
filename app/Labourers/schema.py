import random

import graphene
from Labour.models import LabourService
from Members.models import Member
from Packages.models import LabourersPackage
from Wards.models import Ward
from graphene_django import DjangoObjectType

from .models import Labourer


class LabourerType(DjangoObjectType):
    class Meta:
        model = Labourer


class Query(graphene.ObjectType):
    labourers = graphene.List(LabourerType)

    def resolve_agents(self, info, email=None):
        labourers = Labourer.objects.all()

        return labourers


def getValidAccount():
    while True:
        account = f"LR{random.randint(0, 9)}{random.randint(80, 999)}{random.randint(50, 999)}"
        if not Labourer.objects.filter(account=account).exists():
            return account


class createLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        name = graphene.String(required=True)
        ward = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)
        owner = graphene.Int(required=True)
        packageId = graphene.Int(required=True)

    def mutate(self, info, name, ward, services, owner, packageId):
        labourer = Labourer(name=name)
        ward = Ward.objects.get(id=ward)
        package = LabourersPackage.objects.get(id=packageId)
        owner = Member.objects.get(id=owner)

        LServices = []
        for Service in services:
            service = LabourService.objects.get(id=Service)
            LServices.append(service)

        labourer.ward = ward
        labourer.owner = owner
        if packageId == 1:
            labourer.active = True;
        labourer.package = package
        labourer.account = getValidAccount()
        labourer.save()
        labourer.services.set(LServices)
        labourer.save()

        return createLabourer(labourer=labourer)


class UpdateLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        labourerId = graphene.Int(required=True)
        packageId = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)

    def mutate(self, info, labourerId, packageId, services):
        labourer = Labourer.objects.get(id=labourerId)
        package = LabourersPackage.objects.get(id=packageId)
        l_services = []
        for Service in services:
            service = LabourService.objects.get(id=Service)
            l_services.append(service)

        labourer.services.set(l_services)
        labourer.package = package
        labourer.active = False

        labourer.save()
        return UpdateLabourer(labourer=labourer)


class Mutation(graphene.ObjectType):
    create_Labourer = createLabourer.Field()
    update_Labourer = UpdateLabourer.Field()
