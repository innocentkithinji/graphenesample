from .models import Chat
from Farm.models import Farm
from Buyer.models import Buyer
import graphene
from graphene_django import DjangoObjectType


class ChatType(DjangoObjectType):
    class Meta:
        model = Chat


class Query(graphene.ObjectType):
    chats = graphene.List(ChatType)

    def resolve_chats(self, info):
        return Chat.objects.all()


class AddChat(graphene.Mutation):
    chat = graphene.Field(ChatType)

    class Arguments:
        BuyerId = graphene.Int(required=True)
        SellerId = graphene.Int(required=True)
        DocId = graphene.String(required=True)

    def mutate(self, info, BuyerId, SellerId, DocId):
        buyer = Buyer.objects.get(id=BuyerId)
        seller = Farm.objects.get(id=SellerId)

        chat = Chat(partyA=buyer, partyB=seller, docId=DocId)

        chat.save()

        return AddChat(chat=chat)


class Mutation(graphene.ObjectType):
    addChat = AddChat.Field()
