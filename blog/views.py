from django.shortcuts import render, Http404, redirect
from .forms import blogForm
import os
from bbjWebsite import settings
import json
from markdown import markdown

path = settings.BASE_DIR

# Create your views here.
def index(request):
    username = request.COOKIES.get('username')
    add = False
    if username != None:
        add = True
    context = {
        'nav': True,
        'canpost': add,
    }
    return render(request, 'blog.html', context)


def new(request):
    if request.COOKIES.get('username') == None:
        return Http404
    if request.method == 'POST': 
        form = blogForm(request.POST, request.FILES) 
        if form.is_valid(): 
            body = form.cleaned_data['body']
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            title, description, body = markdown(title), markdown(description), markdown(body)
            checkjson()
            file = os.path.join(path, 'json', 'blog.json')
            with open(file, 'r') as f:
                if f.read() == '':
                    data = {title: [body, description]}
                    with open(file, 'w') as e:
                        json.dump(data, e)
                else:
                    with open(file, 'r') as e:
                        data = json.load(e)
                    if title in data:
                        title = title + ' [1]'
                    data[title] = [body, description]
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

def checkjson():
    if 'json' not in os.listdir(path):
        os.mkdir(os.path.join(path, 'json'))
    if 'blog.json' not in os.listdir(os.path.join(path, 'json')):
        open(os.path.join(path, 'json', 'blog.json'), 'w+')
