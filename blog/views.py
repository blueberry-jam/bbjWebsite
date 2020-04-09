from django.shortcuts import render, Http404, redirect
from .forms import blogForm
import os
from bbjWebsite import settings
import json
from markdown import markdown
import datetime

path = settings.BASE_DIR

# Create your views here.
def index(request):
    username = request.COOKIES.get('username')
    add = False
    if username != None:
        add = True
    checkjson()
    file = os.path.join(path, 'json', 'blog.json')
    with open(file, 'r') as e:
        data = json.load(e)
    order = reversed([key for key in data])
    posts = {}
    for key in order:
        posts[key] = data[key]
    context = {
        'nav': True,
        'canpost': add,
        'posts': posts,
    }
    return render(request, 'blog.html', context)


def new(request):
    if request.COOKIES.get('username') == None:
        raise Http404()
    if request.method == 'POST': 
        form = blogForm(request.POST, request.FILES) 
        if form.is_valid(): 
            body = form.cleaned_data['body']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            body = markdown(body)
            checkjson()
            file = os.path.join(path, 'json', 'blog.json')
            with open(file, 'r') as e:
                data = json.load(e)
            if title in data:
                title = title + ' [1]'
            link = title.split()
            if len(link) > 1:
                link = [link+'+' for link in link]
                link = ''.join(link)
                link = link[:-1]
            else:
                link = title
            today = datetime.date.today()
            date = today.strftime("%m/%d/%y")
            data[title] = [body, description, link, date]
            with open(file, 'w') as e:
                json.dump(data, e)
            return redirect('/blog')
    else:
        form = blogForm()
    context = {
        'nav': True,
        'form': form
    }
    return render(request, 'new.html', context)

def view_post(request, name):
    username = request.COOKIES.get('username')
    add = False
    if username != None:
        add = True
    checkjson()
    file = os.path.join(path, 'json', 'blog.json')
    with open(file, 'r') as e:
        data = json.load(e)
    if name not in data:
        raise Http404()
    data = data[name]
    context = {
        'nav': True,
        'data': data,
        'name': name,
    }
    return render(request, 'post.html', context)


def checkjson():
    if 'json' not in os.listdir(path):
        os.mkdir(os.path.join(path, 'json'))
    if 'blog.json' not in os.listdir(os.path.join(path, 'json')):
        with open(os.path.join(path, 'json', 'blog.json'), 'w') as e:
            json.dump({}, e)
    else:
        e = open(os.path.join(path, 'json', 'blog.json'), 'r').read()
        if e == '':
            with open(os.path.join(path, 'json', 'blog.json'), 'w') as e:
                json.dump({}, e)
        