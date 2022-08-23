from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('search', views.search,name='search'),
    path('contact', views.contact,name='contact'),
    path('about', views.about,name='about'),
    path('signup', views.handleSignUp,name='signup'),
    path('login', views.handleLogIn,name='login'),
    path('logout', views.handleLogOut,name='logout'),
]