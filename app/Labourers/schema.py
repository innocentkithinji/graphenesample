from County.models import County
from Labour.models import LabourService
from Packages.models import LabourersPackage
from Wards.models import Ward
from .models import Labourer
import graphene
from graphene_django import DjangoObjectType


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
        county = graphene.Int(required=True)
        ward = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)
        packageId = graphene.Int(required=True)

    def mutate(self, info, name, county, ward, services, packageId):
        labourer = Labourer(name=name)
        county = County.objects.get(id=county)
        ward = Ward.objects.get(id=ward)
        package = LabourersPackage.objects.get(id=packageId)

        LServices = []
        for Service in services:
            service = LabourService.objects.get(id=Service)
            LServices.append(service)

        labourer.services = LServices
        labourer.ward = ward
        labourer.county = county
        labourer.package = package
        labourer.save()

        return createLabourer(labourer=labourer)


class Mutation(graphene.ObjectType):
    create_Labourer = createLabourer.Field()
