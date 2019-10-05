from ast import literal_eval

from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

# Create your views here.
@require_POST
@csrf_exempt
def mpesa_called_back(request):
    response = request.body
    print(response)
    return HttpResponse(status=200)


@require_POST
@csrf_exempt
def mpesa_validation(request):
    response = request.body
    print(response)
    return HttpResponse(status=200)


@require_POST
@csrf_exempt
def mpesa_confirmation(request):
    response = request.body
    recieved = json.loads(response)
    # {'TransactionType': '', 'TransID': 'NJ551HAKRP', 'TransTime': '20191005161329', 'TransAmount': '300.00',
    #  'BusinessShortCode': '600755', 'BillRefNumber': 'BY6543211', 'InvoiceNumber': '', 'OrgAccountBalance': '',
    #  'ThirdPartyTransID': '', 'MSISDN': '254708374149', 'FirstName': 'John', 'MiddleName': 'J.', 'LastName': 'Doe'}
    ac = recieved["BillRefNumber"][:2]
    if ac == "BY":
        print("Buyer")
    if ac == "FM":
        print("Farmer")
    if ac == "LR":
        print("Labourer")
    return HttpResponse(status=200)
