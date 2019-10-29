import base64
import random
from datetime import datetime

import graphene
import requests
from Labour.models import LabourService
from Members.models import Member
from Packages.models import LabourersPackage
from Wards.models import Ward
from graphene_django import DjangoObjectType
from requests.auth import HTTPBasicAuth

from Mpesa import keys
from Mpesa.models import payRequest
from .models import Labourer


class LabourerType(DjangoObjectType):
    class Meta:
        model = Labourer


class Query(graphene.ObjectType):
    labourers = graphene.List(LabourerType)

    def resolve_agents(self, info, email=None):
        labourers = Labourer.objects.all()

        return labourers


def getValidAccount():
    while True:
        account = f"LR{random.randint(0, 9)}{random.randint(80, 999)}{random.randint(50, 999)}"
        if not Labourer.objects.filter(account=account).exists():
            return account


class createLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        name = graphene.String(required=True)
        ward = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)
        owner = graphene.Int(required=True)
        packageId = graphene.Int(required=True)

    def mutate(self, info, name, ward, services, owner, packageId):
        labourer = Labourer(name=name)
        ward = Ward.objects.get(id=ward)
        package = LabourersPackage.objects.get(id=packageId)
        owner = Member.objects.get(id=owner)

        LServices = []
        for Service in services:
            service = LabourService.objects.get(id=Service)
            LServices.append(service)

        labourer.ward = ward
        labourer.owner = owner
        if packageId == 1:
            labourer.active = True;
        labourer.package = package
        labourer.account = getValidAccount()
        labourer.save()
        labourer.services.set(LServices)
        labourer.save()

        return createLabourer(labourer=labourer)


class UpdateLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        labourerId = graphene.Int(required=True)
        packageId = graphene.Int(required=True)
        services = graphene.List(required=True, of_type=graphene.Int)

    def mutate(self, info, labourerId, packageId, services):
        labourer = Labourer.objects.get(id=labourerId)
        package = LabourersPackage.objects.get(id=packageId)
        l_services = []
        for Service in services:
            service = LabourService.objects.get(id=Service)
            l_services.append(service)

        labourer.services.set(l_services)
        labourer.package = package
        labourer.active = False

        labourer.save()
        return UpdateLabourer(labourer=labourer)


class UpgradeLabourer(graphene.Mutation):
    labourer = graphene.Field(LabourerType)

    class Arguments:
        labourer_id = graphene.Int(required=True)
        package_id = graphene.Int()
        amount = graphene.Int()
        phone = graphene.String()
        acc = graphene.String()

    def mutate(self, info, labourer_id, package_id, amount, phone, acc):
        labourer = LabourService.objects.get(id=labourer_id)
        package = LabourersPackage.objects.get(id=package_id)
        labourer.package = package
        labourer.active = False
        labourer.save()

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

        return UpgradeLabourer(labourer=labourer)


class Mutation(graphene.ObjectType):
    create_Labourer = createLabourer.Field()
    update_Labourer = UpdateLabourer.Field()
