import random

from django.db.models import Q
from .models import Agent
import graphene
from graphene_django import DjangoObjectType


class AgentsType(DjangoObjectType):
    class Meta:
        model = Agent


class Query(graphene.ObjectType):
    agents = graphene.List(AgentsType, email=graphene.String())

    def resolve_agents(self, info, email=None):
        agents = Agent.objects.all()

        if email:
            filterz = (
                Q(email__icontains=email)
            )
            agents = agents.filter(filterz)

        return agents


class CreateAgent(graphene.Mutation):
    agent = graphene.Field(AgentsType)

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    def genRandomUniqueCode(self):
        x = random.randint(1, 999999)
        ag = Agent.objects.get(code=x)
        if ag:
            return self.genRandomUniqueCode()
        else:
            return x

    def mutate(self, info, name, email):
        agent = Agent(name=name, email=email)

        agent.code = self.genRandomUniqueCode()

        agent.save()

        return CreateAgent(agent=agent)


class Mutation(graphene.ObjectType):
    create_Agent = CreateAgent.Field()
