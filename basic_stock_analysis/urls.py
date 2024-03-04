from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
router = routers.DefaultRouter()



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('base.urls')),
    path('api-token-key',obtain_auth_token)
]
urlpatterns+=router.urls