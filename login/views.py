from django.shortcuts import render, Http404
import requests
from bbjWebsite import settings
import os
import json
from .secrets import client_id, secret, client_id_local, secret_local
import datetime
import random
from blog import views as blog
from bbjWebsite import settings
import json

path = settings.BASE_DIR

def index(request):    
    if request.META['HTTP_HOST'] == 'localhost:8000':
        c_id = client_id_local
    else:
        c_id = client_id
    mode = 'login'
    context = {'mode': mode, 'id': c_id}
    return render(request, 'login.html', context)

def logout(request):
    mode = 'logout'    
    context = {'mode': mode, 'nav': True}
    response = render(request, 'login.html', context)
    user_id = request.COOKIES.get('user_id')
    file = os.path.join(settings.BASE_DIR, 'json', 'user_ids.json')
    blog.checkjson('user_ids.json')
    with open(file, 'r') as f:
        data = json.load(f)
    if user_id not in data:
        raise Http404()
    del data[user_id]
    with open(file, 'w') as f:
        json.dump(data, f)
    response.delete_cookie('user_id')
    return response

def loggedIn(request):
    global secret
    if request.META['HTTP_HOST'] == 'localhost:8000':
        c_id = client_id_local
        secret = secret_local
    else:
        c_id = client_id
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
    file = os.path.join(settings.BASE_DIR, 'json', 'user_ids.json')
    if token != 'bad_verification_code':
        username = requests.get('https://api.github.com/user', headers = {'Authorization': 'token {}'.format(token)}).json()['login']
        context['username'] = username
        response = render(request, 'logged-in.html', context)
        if username not in ['jamckson', 'GreerPage', 'tteeoo']:
            raise Http404()
        user_id = [random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNOPQRSTUVWXYZ123456789!@#$%^&') for i in range(30)]
        user_id = ''.join(user_id)
        response.set_cookie('user_id', user_id)
        blog.checkjson('user_ids.json')
        with open(file, 'r') as f:
            data = json.load(f)
        keys = []
        for key in data:
            if data[key] == username:
                keys.append(key)
        for key in keys:
            del data[key]
        with open(file, 'w') as f:
            data[user_id] = username
            json.dump(data, f)
        return response
    else:
        with open(file, 'r') as f:
            data = json.load(f)
        u_id = request.COOKIES.get('user_id')
        if u_id == None:
            raise Http404()
        context['username'] = data[request.COOKIES.get('user_id')]
    return render(request, 'logged-in.html', context)

