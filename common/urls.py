from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path('', views.main, name='main'), 
    path('login/', views.loginview, name='login'), 
    path('signup/', views.signup, name='signup'), 
]