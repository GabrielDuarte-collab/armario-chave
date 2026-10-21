from django.shortcuts import render
from django.http import JsonResponse


def index(request):
    context = {
        'titulo': 'Armario de chaves',
        'Nome': 'Wesley',
    }
    return render(request, 'index.html', context)
# Create your views here.from django.http import JsonResponse


def status_api(request):
    return JsonResponse({'status': 'online', 'sistema': 'key track Iot'})
