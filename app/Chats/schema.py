from .models import Chat
import graphene
from graphene_django import DjangoObjectType


class ChatType(DjangoObjectType):
    class Meta:
        model = Chat


class Query(graphene.ObjectType):
    chats = graphene.List(ChatType)

    def resolve_chats(self, info):
        return Chat.objects.all()
