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
    print(recieved)
    return HttpResponse(status=200)
