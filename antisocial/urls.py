"""antisocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import include, path

from . import views


branding_urls = [
    path('profile_pic', views.ProfilePic.as_view()),
]

urlpatterns = [
    path('', views.HomePage.as_view()),
    path('posts/<pk>', views.SinglePost.as_view()),
    path('branding/', include(branding_urls)),
    path('admin/', admin.site.urls),
]
