
from django.db import connection
from django.shortcuts import render
from django.http import JsonResponse
from .utils import buscar_status_nichos_banco


def index(request):
    context = {
        'titulo': 'Armario de chaves',
        'Nome': 'Wesley',
    }
    return render(request, 'index.html', context)


def status_api(request):
    return JsonResponse({
        'status': 'online',
        'sistema': 'key track Iot'
    })


def status_nichos_view(request):
    nichos = buscar_status_nichos_banco()
    return JsonResponse(nichos, safe=False, status=200)
