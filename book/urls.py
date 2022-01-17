from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    # profile
    path('users/<int:user_id>',views.ProfileView.as_view(),name='profile'),
    path('set-profile/',views.ProfileSetView.as_view(),name='profile-set'),
    path('edit-profile/',views.ProfileUpdateView.as_view(),name='profile-update'),
]