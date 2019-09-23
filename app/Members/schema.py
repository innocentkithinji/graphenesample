from django.db.models import Q

from .models import Member
import graphene
from graphene_django import DjangoObjectType
from Agent.models import Agent

class MemberType(DjangoObjectType):
    class Meta:
        model = Member


class Query(graphene.ObjectType):
    members = graphene.List(MemberType, uid=graphene.String(), phone=graphene.String())
    members_phone = graphene.List(MemberType, phone=graphene.String())

    def resolve_members(self, info, uid=None, phone=None):
        mbr = Member.objects.all()

        if uid:
            filters = (
                Q(uid__icontains=uid)
            )
            mbr = mbr.filter(filters)

        if phone:
            filters = (
                Q(phoneNumber__icontains=phone)
            )

            mbr = mbr.filter(filters)

        return mbr

    def resolve_members_phone(self, info, phone=None):
        mbr = Member.objects.all()

        if phone:
            filters = (
                Q(phoneNumber__icontains=phone)
            )

            mbr = mbr.filter(filters)
        return mbr


class createUser(graphene.Mutation):
    member = graphene.Field(MemberType)

    class Arguments:
        phoneNumber = graphene.String(required=True)
        uid = graphene.String(required=True)
        fcm_id = graphene.String(required=True)
        agent_code = graphene.Int()

    def mutate(self, info, phoneNumber, uid, fcm_id, agent_code=None):
        member = Member(phoneNumber=phoneNumber, uid=uid, fcm_id=fcm_id)
        if agent_code:
            agent = Agent.objects.get(code=agent_code)
            print(agent)
            member.agent = agent

        member.save()

        return createUser(member=member)


class updateUser(graphene.Mutation):
    member = graphene.Field(MemberType)

    class Arguments:
        memberId = graphene.Int(required=True)
        phoneNumber = graphene.String()
        uid = graphene.String()
        fcm_id = graphene.String()

    def mutate(self, info, memberId, phoneNumber=None, uid=None, fcm_id=None):
        member = Member.objects.get(id=memberId)

        if phoneNumber:
            member.phoneNumber = phoneNumber
        if uid:
            member.uid = uid
        if fcm_id:
            member.fcm_id = fcm_id

        member.save()

        return updateUser(member=member)


class Mutation(graphene.ObjectType):
    create_user = createUser.Field()
    update_user = updateUser.Field()
