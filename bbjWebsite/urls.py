"""bbjWebsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homepage import views as viewshome
from . import views as rootviews
from about import views as about
from login import views as login
from blog import views as blog

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', viewshome.index),
    path('about', about.index),
    path('about/', rootviews.noSlash),
    path('blog', blog.index),
    path('blog/', rootviews.noSlash),
    path('login', login.index),
    path('logged-in', login.loggedIn),
    path('new/blog', blog.new),
    path('logout', login.logout),
    path('blog/<str:name>', blog.view_post),
    path('blog/edit/<str:name>', blog.edit),
]

handler404 = rootviews.error_404
handler500 = rootviews.error_500
handler403 = rootviews.error_403
handler400 = rootviews.error_400