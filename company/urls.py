"""
URL configuration for bill_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from .views import *

urlpatterns = [
    path('login', Login.as_view(), name='check'),
    path('register', Register.as_view(), name='register'),

    # company

    # company/ :post: create company {}
    # company/ :get: list all company : [{},{},{}]
    # company/<id>/ :get:  object  {}
    # company/<id>/ :patch:  object  {}
    # company/<id>/ :delete:  ""

    path('company', Companyview.as_view(), name='company'),
    path('company/<int:id>', Updatecompanyview.as_view(), name="update_company"),

    path('client', Clientview.as_view(), name='client'),
    path('client/<int:id>', Updateclientview.as_view(), name='client'),
]
