from django.urls import path
from . import views

urlpatterns = [
    path('',views.main,name='main'),
    # profile
    path('users/<int:user_id>',views.ProfileView.as_view(),name='profile'),
    path('set-profile/',views.ProfileSetView.as_view(),name='profile-set'),
    path('edit-profile/',views.ProfileUpdateView.as_view(),name='profile-update'),
   
    # account
    path('login/', views.loginview, name='login'), 
    path('signup/', views.signup, name='signup'), 
]