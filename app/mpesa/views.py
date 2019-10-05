from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.
@require_POST
@csrf_exempt
def mpesa_called_back(request):
    response = request.body
    print(response)
    return HttpResponse(status=200)