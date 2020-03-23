from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'nav': True,
    }
    return render(request, 'software.html', context)