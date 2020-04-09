from django.shortcuts import render, Http404
import requests
from bbjWebsite import settings
import os
import json
from .secrets import client_id, secret, client_id_local, secret_local
import datetime

path = settings.BASE_DIR

def index(request):    
    if request.META['HTTP_HOST'] == 'localhost:8000':
        c_id = client_id_local
    else:
        c_id = client_id
    if request.path == '/login':
        mode = 'login'
        context = {'mode': mode, 'id': c_id}
        return render(request, 'login.html', context)
    if request.path == '/logout':
        mode = 'logout'    
        context = {'mode': mode, 'nav': True}
        response = render(request, 'login.html', context)
        response.delete_cookie('username')
        return response

def loggedIn(request):
    if request.META['HTTP_HOST'] == 'localhost:8000':
        c_id = client_id_local
        secret = secret_local
    else:
        c_id = client_id
        secret = secret
    code = request.GET.get('code')
    response = requests.post('https://github.com/login/oauth/access_token', data = {
        'client_id': c_id,
        'client_secret': secret,
        'code': code,
        'accept': 'json'
    }).content.decode('Utf-8')
    response = response.split('=')[1]
    token = response.split('&')[0]
    context = {'nav': True}
    if token != 'bad_verification_code':
        username = requests.get('https://api.github.com/user', headers = {'Authorization': 'token {}'.format(token)}).json()['login']
        context['username'] = username
        response = render(request, 'logged-in.html', context)
        if username not in ['jamckson', 'GreerPage', 'tteeoo']:
            return Http404()
        response.set_cookie('username', username)
        return response
    else:
        context['username'] = request.COOKIES.get('username')
    return render(request, 'logged-in.html', context)

