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

    def mutate(self, info, buyer_id, seller_id, doc_id):
        buyer = Buyer.objects.get(id=buyer_id)
        seller = Farm.objects.get(id=seller_id)

        chat = Chat(partyA=buyer, partyB=seller, docId=doc_id)

        chat.save()

        return AddChat(chat=chat)


class Mutation(graphene.ObjectType):
    addChat = AddChat.Field()
