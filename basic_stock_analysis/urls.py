from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from base import views as base_views
router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('base.urls')),
    path('',  include('api.urls')),
    path('api-token-auth',obtain_auth_token)
]
urlpatterns+=router.urls