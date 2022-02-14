"""django_ninja URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from typing import Dict

from django.contrib import admin
from django.http import HttpRequest
from django.urls import path
from ninja import NinjaAPI

from tabom.apis.v1.article_router import router as article_router
from tabom.apis.v1.like_router import router as like_router

api = NinjaAPI()
api.add_router("/likes", like_router)
api.add_router("/articles/", article_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
