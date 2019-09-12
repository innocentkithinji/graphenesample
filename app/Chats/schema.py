from .models import Chat
from Farm.models import Farm
from Buyer.models import Buyer
import graphene
from graphene_django import DjangoObjectType
from pyfcm import FCMNotification


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


class SendNotification(graphene.Mutation):
    chat = graphene.Field(ChatType)

    class Arguments:
        partyId = graphene.Int(required=True)
        type = graphene.String(required=True)
        Message = graphene.String(required=True)
        title = graphene.String(required=True)
        action = graphene.String(required=True)

    def mutate(self, info, partyId, type, Message, title, action):
        buyer = Buyer.objects.get(id=partyId)
        push = FCMNotification(
            api_key="AAAAr7bm4Pw:APA91bGzMCMzPkoSPvqXkbSFGe5cRBjMDWRKV8tIkVGg76UwcYARrmMWrQjkx9fDsG"
                    "GcrrfcDbkLuhvmmeDtzPsdW22MnNzND_14rEMVTLOpGXL67G8tj88sKQrKrs0iIhWxXwqGEbiA")
        regid = buyer.owner.fcm_id
        print(regid)
        # regid = "e7vP0PmAWio:APA91bFZq1kVw7sNo6xee1FJPuxQ69GQm6R-H5G8jmt5c1Pf1a6fyFDqgJqsKSk99gc1OFGVnKnIRt6r6KLYi8-JPXyLULzctALTsS-aItsrmZ3MsX6BCqExEFVKigFME7vyz9hankNm"
        result = push.notify_single_device(registration_id=regid, message_title=title, message_body=Message)

        return result


class Mutation(graphene.ObjectType):
    addChat = AddChat.Field()
    notify = SendNotification.Field()
