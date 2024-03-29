from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('',views.home,name="home"),
    path('newcompany/',views.getNewCompany,name="newcompany"),
    path('company/',views.companyRoom,name="companyRoom"),
    path('user/',views.userPage,name='userRoom'),
    path('reset_token/',views.reset_token, name='reset_token')
]
