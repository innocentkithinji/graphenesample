from django.db.models import Q

from .models import Member
import graphene
from graphene_django import DjangoObjectType


class MemberType(DjangoObjectType):
    class Meta:
        model = Member


class Query(graphene.ObjectType):
    members = graphene.List(MemberType, uid=graphene.String())

    def resolve_members(self, info, uid=None):
        mbr = Member.objects.all()

        if uid:
            filters = (
                Q(uid__icontains=uid)
            )
            mbr = mbr.filter(filters)

        return mbr


class createUser(graphene.Mutation):
    member = graphene.Field(MemberType)

    class Arguments:
        phoneNumber = graphene.String(required=True)
        uid = graphene.String(required=True)
        fcm_id = graphene.String(required=True)

    def mutate(self, info, phoneNumber, uid, fcm_id):
        member = Member(phoneNumber=phoneNumber, uid=uid, fcm_id=fcm_id)
        member.save()

        return createUser(member=member)


class updateUser(graphene.Mutation):
    member = graphene.Field(MemberType)

    class Arguments:
        memberId = graphene.Int(required=True)
        phoneNumber = graphene.String()
        uid = graphene.String()
        fcm_id = graphene.String()

    def mutate(self, info, memberId, phoneNumber, uid, fcm_id):
        member = Member.objects.get(id=memberId)

        member.phoneNumber = phoneNumber
        member.uid = uid
        member.fcm_id = fcm_id

        return updateUser(member=member)


class Mutation(graphene.ObjectType):
    create_user = createUser.Field()
    update_user = updateUser.Field()
