from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib import admin
from django.conf.urls.static import static


urlpatterns =[
	path('home/',views.home),
    path('login/', views.facelogin),
    path('signup/', views.signup_call),
    path('logout/', views.logout_call),


]


