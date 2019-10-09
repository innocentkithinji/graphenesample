import json

from Buyer.models import Buyer
from Farm.models import Farm
from Labourers.models import Labourer
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import paymentMade


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
    recieved = json.loads(response)
    # {'TransactionType': '', 'TransID': 'NJ551HAKRP', 'TransTime': '20191005161329', 'TransAmount': '300.00',
    #  'BusinessShortCode': '600755', 'BillRefNumber': 'BY6543211', 'InvoiceNumber': '', 'OrgAccountBalance': '',
    #  'ThirdPartyTransID': '', 'MSISDN': '254708374149', 'FirstName': 'John', 'MiddleName': 'J.', 'LastName': 'Doe'}
    ac = recieved["BillRefNumber"][:2]
    pay = paymentMade()
    pay.transactionID = recieved["TransID"]
    pay.time = recieved["TransTime"]
    pay.transAmount = int(float(recieved["TransAmount"]))
    pay.accountRef = recieved["BillRefNumber"]
    pay.phone = recieved["MSISDN"]
    pay.payer = f"{recieved['FirstName']} {recieved['LastName']}"

    pay.save()

    if ac == "BY":
        print("Buyer")
        buyer = Buyer.objects.get(account=recieved["BillRefNumber"])
        if int(float(recieved["TransAmount"])) >= buyer.package.price:
            print("Conf")
            buyer.active = True
        else:
            print("None")
        buyer.save()

    if ac == "FM":
        print("Farmer")
        farm = Farm.objects.get(account=recieved["BillRefNumber"])
        if int(float(recieved["TransAmount"])) >= farm.package.price:
            farm.active = True
        farm.save()

    if ac == "LR":
        print("Labourer")
        labourer = Labourer.objects.get(account=recieved["BillRefNumber"])
        if int(float(recieved["TransAmount"])) >= labourer.package.price:
            labourer.active = True
        labourer.save()

    return HttpResponse(status=200)


@require_POST
@csrf_exempt
def mpesa_confirmation(request):
    response = request.body
    recieved = json.loads(response)
    print(recieved)
    # {'TransactionType': '', 'TransID': 'NJ551HAKRP', 'TransTime': '20191005161329', 'TransAmount': '300.00',
    #  'BusinessShortCode': '600755', 'BillRefNumber': 'BY6543211', 'InvoiceNumber': '', 'OrgAccountBalance': '',
    #  'ThirdPartyTransID': '', 'MSISDN': '254708374149', 'FirstName': 'John', 'MiddleName': 'J.', 'LastName': 'Doe'}
    ac = recieved["BillRefNumber"][:2]
    pay = paymentMade()
    pay.transactionID = recieved["TransID"]
    pay.time = recieved["TransTime"]
    pay.transAmount = int(float(recieved["TransAmount"]))
    pay.accountRef = recieved["BillRefNumber"]
    pay.phone = recieved["MSISDN"]
    pay.payer = f"{recieved['FirstName']} {recieved['LastName']}"

    pay.save()

    if ac == "BY":
        print("Buyer")
        buyer = Buyer.objects.get(account=recieved["BillRefNumber"])
        if int(float(recieved["TransAmount"])) >= buyer.package.price:
            print("Conf")
            buyer.active = True
        else:
            print("None")
        buyer.save()

    if ac == "FM":
        print("Farmer")
        farm = Farm.objects.get(account=recieved["BillRefNumber"])
        if int(float(recieved["TransAmount"])) >= farm.package.price:
            farm.active = True
        farm.save()

    if ac == "LR":
        print("Labourer")
        labourer = Labourer.objects.get(account=recieved["BillRefNumber"])
        if int(float(recieved["TransAmount"])) >= labourer.package.price:
            labourer.active = True
        labourer.save()

    return HttpResponse(status=200)


def redirectTo(request):
    return HttpResponseRedirect("https://hayvest.com")