from django.urls.conf import path
from . import views

urlpatterns = [
    path('', views.Landing, name="mainpage"),
    path('login/', views.LoginSignup, name="loginsignuppage"),
    path('home/', views.Home, name="homepage"),
    path('logout/', views.LogoutUser, name="logoutpage"),
    path('managecontent/', views.ManageContent, name="managecontentpage")
]