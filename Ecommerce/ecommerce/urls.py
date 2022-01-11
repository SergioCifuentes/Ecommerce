"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from . import views
app_name ='ecommerce'
urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'signin/',
        views.signin,
        name='signin'
    ),
    path(
        'signup/',
        views.signup,
        name='signup'
    ),
    path(
        'lista_productos/',
        views.lista_productos,
        name='lista_productos'
    ),
    path(
        'agregar_producto/',
        views.agregar_producto,
        name='agregar_producto'
    ),
    path(
        'comprar_producto/<int:id>', 
        views.comprar_producto, 
        name='comprar_producto'
    ),
    
]
