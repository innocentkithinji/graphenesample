import datetime

import graphene
from graphene_django import DjangoObjectType

from .models import  LabourApplication


class LabourApplicationType(DjangoObjectType):
    class Meta:
        model = LabourApplication


class Query(graphene.ObjectType):
    applications = graphene.List(LabourApplicationType, RequestId=graphene.Int(required=True))

    def resolve_applications(self, info, RequestId):
        request = LaboursRequest.objects.get(id=RequestId)
        applications = LabourApplication.objects.filter(LaboursRequest=request)

        return applications


class makeApplication(graphene.Mutation):
    application = graphene.Field(LabourApplicationType)

    class Arguments:
        LabourRequest = graphene.Int(required=True)
        LabourerId = graphene.Int(required=True)

    def mutate(self, info, LabourRequest, LabourerId):
        LabourReq = LaboursRequest.objects.get(id=LabourRequest)
        labourer = Labourer.objects.get(id=LabourerId)

        application = LabourApplication()
        application.Labourer = labourer
        application.LaboursRequest = LabourReq
        application.hired = False

        application.save()

        return makeApplication(application=application)


class RespondApplication(graphene.Mutation):
    application = graphene.Field(LabourApplicationType)

    class Arguments:
        LabourApply = graphene.Int(required=True)
        hiring = graphene.Boolean(required=True)

    def mutate(self, info, LabourApply, hiring):
        application = LabourApplication.objects.get(id=LabourApply)
        application.hired = hiring
        application.responded = True

        application.save()

        return RespondApplication(application=application)


class Mutation(graphene.ObjectType):
    make_Application = makeApplication.Field()
    respond_to_Application = RespondApplication.Field()
