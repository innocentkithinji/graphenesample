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


class CreateLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        name = graphene.String(required=True)
        county = graphene.Int(required=True)
        ward = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)
        packageId = graphene.Int(required=True)

    def mutate(self, info):
        pass
