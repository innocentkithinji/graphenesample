import base64

import requests
from django.db.models import Q
from requests.auth import HTTPBasicAuth

from Mpesa import keys
from .models import payRequest
import graphene
from graphene_django import DjangoObjectType
from datetime import datetime


class payRequestType(DjangoObjectType):
    class Meta:
        model = payRequest


class Query(graphene.ObjectType):
    payRequest = graphene.List(payRequestType)

    def resolve_payRequest(self, info):
        return payRequest.objects.all()


class createPayRequest(graphene.Mutation):
    payReq = graphene.Field(payRequestType)

    class Arguments:
        phone = graphene.String()
        acc = graphene.String()
        amount = graphene.Int()

    def mutate(self, info, phone, acc, amount):
        payReq = payRequest(phone=phone, amount=amount, account=acc)
        auth_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        r = requests.get(auth_URL, auth=HTTPBasicAuth(keys.consumer_key, keys.consumer_secret))
        response = r.json()
        print(response)
        access_token = response['access_token']

        rawtime = datetime.now()
        finishedtime = rawtime.strftime("%Y%m%d%H%M%S")
        rawpass = "{}{}{}".format(keys.business_short_code, keys.passKey, finishedtime)
        print(rawpass)
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
            "AccountReference":acc,
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

        return createPayRequest(payReq=payReq)


class Mutation(graphene.ObjectType):
    mpesaPay = createPayRequest.Field()