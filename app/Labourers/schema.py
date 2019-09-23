from County.models import County
from Labour.models import LabourService
from Packages.models import LabourersPackage
from Wards.models import Ward
from Members.models import Member
from .models import Labourer
import graphene
from graphene_django import DjangoObjectType
import random


class LabourerType(DjangoObjectType):
    class Meta:
        model = Labourer


class Query(graphene.ObjectType):
    labourers = graphene.List(LabourerType)

    def resolve_agents(self, info, email=None):
        labourers = Labourer.objects.all()

        return labourers


class createLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        name = graphene.String(required=True)
        ward = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)
        owner = graphene.Int(required=True)
        packageId = graphene.Int(required=True)


    def genRandomUniqueCode(self):
        x = f"LR{random.randint(1, 999999)}"
        print(x)
        ag = Labourer.objects.get(account=x)
        if ag:
            return self.genRandomUniqueCode
        else:
            return x

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
        labourer.package = package
        labourer.account = f"LR{random.randint(1, 999999)}"
        labourer.save()
        labourer.services.set(LServices)
        labourer.save()


        return createLabourer(labourer=labourer)


class Mutation(graphene.ObjectType):
    create_Labourer = createLabourer.Field()
