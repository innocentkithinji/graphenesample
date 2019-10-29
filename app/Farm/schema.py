import base64
import random
from datetime import datetime

import graphene
import requests
from County.models import County
from Members.models import Member
from Packages.models import FarmPackage
from Wards.models import Ward
from graphene_django import DjangoObjectType

from Mpesa.models import payRequest
from requests.auth import HTTPBasicAuth

from Mpesa import keys
from .models import Farm


class FarmType(DjangoObjectType):
    class Meta:
        model = Farm


class Query(graphene.ObjectType):
    farms = graphene.List(FarmType)

    def resolve_farms(self, info):
        return Farm.objects.all()


class CreateFarm(graphene.Mutation):
    farm = graphene.Field(FarmType)

    class Arguments:
        name = graphene.String(required=True)
        county_id = graphene.Int(required=True)
        package_id = graphene.Int(required=True)
        owner_id = graphene.Int(required=True)
        ward_id = graphene.Int(required=True)

    def mutate(self, info, county_id, name, ward_id, package_id, owner_id):
        farm = Farm(name=name)

        county = County.objects.get(id=county_id)
        package = FarmPackage.objects.get(id=package_id)
        owner = Member.objects.get(id=owner_id)
        ward = Ward.objects.get(id=ward_id)

        farm.county = county
        farm.package = package
        farm.owner = owner
        farm.Ward = ward
        farm.account = getValidAccount()
        if package.id == 5:
            farm.active = True

        farm.save()

        return CreateFarm(farm=farm)


def getValidAccount():
    while True:
        account = f"FM{random.randint(0, 9)}{random.randint(80, 999)}{random.randint(50, 999)}"
        if not Farm.objects.filter(account=account).exists():
            return account


class UpdateFarmAccounts(graphene.Mutation):
    farms = graphene.Field(FarmType)

    def mutate(self, info):
        farms = Farm.objects.all()
        theFarm = None;
        for farm in farms:
            f = Farm.objects.get(id=farm.id)
            updateAccount = getValidAccount()
            f.accounts = updateAccount
            f.save()
            theFarm = f

        return UpdateFarmAccounts(farms=theFarm)


class UpdateFarm(graphene.Mutation):
    farm = graphene.Field(FarmType)

    class Arguments:
        farm_id = graphene.Int(required=True)
        name = graphene.String()
        package_id = graphene.Int()
        active = graphene.Boolean()

    def mutate(self, info, farm_id, package_id, active, name=None):
        farm = Farm.objects.get(id=farm_id)
        package = FarmPackage.objects.get(id=package_id)
        if name:
            farm.name = name
        farm.package = package
        farm.active = active
        farm.package_update_date = datetime.now()

        farm.save()

        return UpdateFarm(farm=farm)


class UpgradeFarm(graphene.Mutation):
    farm = graphene.Field(FarmType)

    class Arguments:
        farm_id = graphene.Int(required=True)
        package_id = graphene.Int()
        amount = graphene.Int()
        phone = graphene.String()
        acc = graphene.String()
    
    def mutate(self, info, farm_id, package_id, amount, phone, acc ):
        farm = Farm.objects.get(id=farm_id)
        package = FarmPackage.objects.get(id=package_id)
        farm.package = package
        farm.active = False
        farm.save()

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

        return UpgradeFarm(farm=farm)
    

class Mutation(graphene.ObjectType):
    create_farm = CreateFarm.Field()
    update_farm = UpdateFarm.Field()
    upgrade_farm = UpgradeFarm.Field()

