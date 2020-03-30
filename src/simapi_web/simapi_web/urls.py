"""simapi_web URL Configuration

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
from django.urls import path, include
from rest_framework import routers

from graphene_django.views import GraphQLView
from rest_api import views

router = routers.DefaultRouter()
router.register('user', views.UserViewSet)
router.register('login', views.LoginViewSet, basename='login')
router.register('init_model', views.FmuModelViewSet)
router.register('input', views.InputViewSet)
router.register('output', views.OutputViewSet)
router.register('hostname', views.HostNameViewSet, basename='hostname')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
