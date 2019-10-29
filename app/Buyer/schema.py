import base64
import datetime
import random

import graphene
import requests
from County.models import County
from Members.models import Member
from Packages.models import BuyerPackage
from graphene_django import DjangoObjectType
from requests.auth import HTTPBasicAuth

from app.Mpesa import keys
from app.Mpesa.models import payRequest
from .models import Buyer


class BuyerType(DjangoObjectType):
    class Meta:
        model = Buyer


class Query(graphene.ObjectType):
    buyers = graphene.List(BuyerType)

    def resolve_buyers(self, info):
        return Buyer.objects.all()


def getValidAccount():
    while True:
        account = f"BY{random.randint(0, 9)}{random.randint(111, 999)}{random.randint(222, 999)}"
        if not Buyer.objects.filter(account=account).exists():
            return account


class UpdateBuyerAccounts(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    def mutate(self, info):
        buyers = Buyer.objects.all()
        theBuyer = None
        for buyer in buyers:
            b = Buyer.objects.get(id=buyer.id)
            updateAccount = getValidAccount()
            b.account = updateAccount
            b.save()
            theBuyer = b

        return UpdateBuyerAccounts(buyer=theBuyer)


class CreateBuyer(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    class Arguments:
        name = graphene.String(required=True)
        county_id = graphene.Int(required=True)
        latitude = graphene.Float(required=True)
        longitude = graphene.Float(required=True)
        package_id = graphene.Int(required=True)
        owner_id = graphene.Int(required=True)

    def mutate(self, info, name, county_id, latitude, longitude, package_id, owner_id):
        owner = Member.objects.get(id=owner_id)
        county = County.objects.get(id=county_id)
        package = BuyerPackage.objects.get(id=package_id)

        buyer = Buyer(name=name, latitude=latitude, longitude=longitude)
        buyer.owner = owner
        buyer.county = county
        if package_id == 1:
            buyer.active = True
        buyer.package = package
        buyer.account = getValidAccount()

        buyer.save()

        return CreateBuyer(buyer=buyer)


class UpdateBuyer(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    class Arguments:
        buyer_id = graphene.Int(required=True)
        name = graphene.String()
        package_id = graphene.Int()

    def mutate(self, info, buyer_id, package_id, name=None):
        buyer = Buyer.objects.get(id=buyer_id)
        package = BuyerPackage.objects.get(id=package_id)

        if name:
            buyer.name = name
        buyer.package = package
        buyer.package_update_date = datetime.datetime.now()
        buyer.active = False
        buyer.save()

        return UpdateBuyer(buyer=buyer)


class UpgradeBuyer(graphene.Mutation):
    buyer = graphene.Field(BuyerType)

    class Arguments:
        labourer_id = graphene.Int(required=True)
        package_id = graphene.Int()
        amount = graphene.Int()
        phone = graphene.String()
        acc = graphene.String()

    def mutate(self, info, labourer_id, package_id, amount, phone, acc):
        buyer = Buyer.objects.get(id=labourer_id)
        package = BuyerPackage.objects.get(id=package_id)
        buyer.package = package
        buyer.active = False
        buyer.save()

        payReq = payRequest(phone=phone, amount=amount, account=acc)
        auth_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(auth_URL, auth=HTTPBasicAuth(keys.consumer_key, keys.consumer_secret))
        response = r.json()
        print(response)
        access_token = response['access_token']

        rawtime = datetime.now()
        finishedtime = rawtime.strftime("%Y%m%d%H%M%S")
        rawpass = "{}{}{}".format(keys.business_short_code, keys.passKey, finishedtime)
        base64Pass = base64.b64encode(rawpass.encode())
        passwd = base64Pass.decode()
        phone = "254" + phone[1:]
        stk_api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": keys.business_short_code,
            "Password": passwd,
            "Timestamp": finishedtime,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": keys.business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://payment.hayvest.co.ke/stkcallback",
            "AccountReference": acc,
            "TransactionDesc": "Simple Test"
        }

        response = requests.post(stk_api_url, json=request, headers=headers)
        final_response = response.json()
        print(final_response)

        if 'CheckoutRequestID' in final_response:
            payReq.posted = True
            payReq.checkOutID = final_response["CheckoutRequestID"]
        else:
            payReq.posted = False

        payReq.save()

        return UpgradeBuyer(buyer=buyer)


class Mutation(graphene.ObjectType):
    create_buyer = CreateBuyer.Field()
    update_buyer = UpdateBuyer.Field()
    give_buyers_accounts = UpdateBuyerAccounts.Field()
