from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from base import views as base_views
router = routers.DefaultRouter()
router.register(r'comp',base_views.CompanyViewSet,basename='comp')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('base.urls')),
    path('api-token-auth',obtain_auth_token)
]
urlpatterns+=router.urls