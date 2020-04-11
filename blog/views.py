from django.shortcuts import render, Http404, redirect
from .forms import blogForm, deleteForm
import os
from bbjWebsite import settings
import json
from markdown import markdown
import datetime

path = settings.BASE_DIR

# Create your views here.
def index(request):
    user_id = request.COOKIES.get('user_id')
    file = os.path.join(settings.BASE_DIR, 'json', 'user_ids.json')
    checkjson('user_ids.json')
    with open(file, 'r') as f:
            data = json.load(f)
    add = False
    if user_id in data:
        add = True
    checkjson('blog.json')
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
    user_id = request.COOKIES.get('user_id')
    file = os.path.join(settings.BASE_DIR, 'json', 'user_ids.json')
    checkjson('user_ids.json')
    with open(file, 'r') as f:
            data = json.load(f)
    if user_id not in data:
        raise Http404()
    if request.method == 'POST': 
        form = blogForm(request.POST, request.FILES) 
        if form.is_valid(): 
            body = form.cleaned_data['body']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            mdbody = markdown(body)
            checkjson('blog.json')
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
            data[title] = [mdbody, description, link, date, body]
            with open(file, 'w') as e:
                json.dump(data, e)
            return redirect('/blog')
    else:
        form = blogForm()
    context = {
        'nav': True,
        'form': form,
        'body': '',
        'description': '',
        'title': '',
        't': 'new post',
    }
    return render(request, 'new.html', context)

def view_post(request, name):
    username = request.COOKIES.get('user_id')
    add = False
    link = name
    file = os.path.join(settings.BASE_DIR, 'json', 'user_ids.json')
    checkjson('user_ids.json')
    with open(file, 'r') as f:
            data = json.load(f)
    if username in data:
        add = True
    checkjson('blog.json') 
    file = os.path.join(path, 'json', 'blog.json')
    with open(file, 'r') as e:
        data = json.load(e)
    name = name.replace('+', ' ')
    if name not in data:
        raise Http404()
    if request.method == 'POST': 
        form = deleteForm(request.POST, request.FILES) 
        if form.is_valid(): 
            delete = form.cleaned_data['delete']
            if delete == 'yes':
                del data[name]
                with open(file, 'w') as e:
                    json.dump(data, e)
        return redirect('/blog')
    
    form = deleteForm()
    data = data[name]
    context = {
        'nav': True,
        'data': data,
        'name': name,
        'add': add,
        'form': form,
        'link': link,
    }
    return render(request, 'post.html', context)


def checkjson(name):
    if 'json' not in os.listdir(path):
        os.mkdir(os.path.join(path, 'json'))
    if name not in os.listdir(os.path.join(path, 'json')):
        with open(os.path.join(path, 'json', name), 'w') as e:
            print(e)
            json.dump({}, e)
    else:
        e = open(os.path.join(path, 'json', name), 'r').read()
        if e == '':
            with open(os.path.join(path, 'json', name), 'w') as e:
                json.dump({}, e)

def edit(request, name):
    if request.COOKIES.get('username') == None:
        raise Http404()
    link = name
    name = name.replace('+', ' ')
    file = os.path.join(path, 'json', 'blog.json')
    with open(file, 'r') as e:
        data = json.load(e)
    checkjson('blog.json')
    if request.method == 'POST': 
        form = blogForm(request.POST, request.FILES) 
        if form.is_valid(): 
            body = form.cleaned_data['body']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            mdbody = markdown(body)  
            link = title.split()
            if len(link) > 1:
                link = [link+'+' for link in link]
                link = ''.join(link)
                link = link[:-1]
            else:
                link = title
            if title != name:
                date = data[name][3]
                data[title] = [mdbody, description, link, date, body]
                del data[name]
                with open(file, 'w') as e:
                    json.dump(data, e)
            else:
                date = data[name][3]
                data[title] = [mdbody, description, link, date, body]
                with open(file, 'w') as e:
                    json.dump(data, e)
            return redirect('/blog/{}'.format(link))
    else:
        form = blogForm()
    context = {
        'nav': True,
        'form': form,
        'body': data[name][4],
        'description': data[name][1],
        'title': name,
        't': 'edit'
    }
    return render(request, 'new.html', context)