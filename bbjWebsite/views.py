from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

def error_404(request, exception):
    data = {
        'error': 'page not found',
        'errornum': '404',
    }
    return render(request,'error.html', data)

def error_500(request):
    data = {
        'error': 'internal server error',
        'errornum': '500',
    }
    return render(request,'error.html', data)
def error_400(request, exception):
    data = {
        'error': 'bad request',
        'errornum': '400',
    }
    return render(request,'error.html', data)
def error_403(request, exception):
    data = {
        'error': 'forbidden',
        'errornum': '403',
    }
    return render(request,'error.html', data)