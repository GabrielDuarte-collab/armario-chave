from django.shortcuts import render


def index(request):
    context = {
        'titulo': 'Armario de chaves',
        'Nome': 'Wesley',
    }
    return render(request, 'index.html', context)
# Create your views here.
