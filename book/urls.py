from argparse import Namespace
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

#app_name = 'book'
urlpatterns = [
    path('',views.main,name='main'),
    # profile
    path('users/<int:user_id>',views.ProfileView.as_view(),name='profile'),
    path('set-profile/',views.ProfileSetView.as_view(),name='profile-set'),
    path('edit-profile/',views.ProfileUpdateView.as_view(),name='profile-update'),
    path('wishList-profile/', views.WishList.as_view(), name='profile-wishList'),
   
    # account
    path('login/', views.loginview, name='login'),
    path('signup/', views.signup, name='signup'),

    path('search/', views.search, name='search'),  
    
    path('book/list', views.BookList.as_view()),
    path('book/<int:book_isbn>/', views.bookDetail),
    path('book/like/<int:book_isbn>/', views.addWishList, name='like-book')
]