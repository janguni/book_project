from multiprocessing import context
from django.db.models import Q, Max
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView
)
from book.forms import ProfileForm, ReviewForm
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from book.models import Genre, User, Book, WishBookList, Review, Tag
from book.functions import confirmation_required_redirect
from random import *
import random



def get_random(request):
    # max_id = Book.objects.all().aggregate(max_id=Max("id"))['max_id']
    # while True:
    #     pk = random.randint(1, max_id)
    #     book = Book.objects.filter(pk=pk).first()
    #     if book:
    #         return book
    num = randrange(0,49)
    book1 = Book.objects.filter(genre_name='컴퓨터/모바일')[:50]
    random1 = book1[num]

    return render(request, 'book/random.html',{'random1':random1})


# main
def main(request):
    return render(request, 'book/main.html')


# account/signup
def signup(request):
    if request.method == 'GET':
        form = SignupForm()

    elif request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'account/signup_success.html')
    return render(request, 'account/signup.html', {'form': form})


# account/login
def loginview(request):
    if request.method == 'GET':
        return render(request, 'account/login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # 로그인 성공
            return render(request, 'book/main.html')
        else:
            # 로그인 실패
            return render(request, 'account/login.html', {'error': '아이디 또는 비밀번호를 확인하세요!'})
    else:
        return render(request, 'account/login.html')


# profile
class ProfileView(DetailView):
    model = User
    template_name = 'profile/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')

        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('main')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile/profile_update_form.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('profile', kwargs=({'user_id': self.request.user.id}))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse('profile', kwargs=({'user_id': self.request.user.id}))


def search(request):
    if request.method == "GET":
        search_key = request.GET['q']
        option_select = request.GET.getlist('option_select', None)

        if 'all' in option_select:
            search_books = Book.objects.filter(
                Q(book_title__icontains=search_key) | Q(book_publisher__icontains=search_key) | Q(
                    book_author__icontains=search_key) | Q(genre_name__icontains=search_key))

        elif 'title' in option_select:
            search_books = Book.objects.filter(Q(book_title__icontains=search_key))

        elif 'author' in option_select:
            search_books = Book.objects.filter(Q(book_author__icontains=search_key))

        elif 'publisher' in option_select:
            search_books = Book.objects.filter(Q(book_publisher__icontains=search_key))

        elif 'genre' in option_select:
            search_books = Book.objects.filter(Q(genre_name__icontains=search_key))

        return render(request, 'book/search.html', {'search_books': search_books, 'search_key': search_key})

    else:
        return render(request, 'book/main.html')


# 장르선택
class GenreList(ListView):
    model = Genre
    template_name = 'book/select_genre.html'


def SelectedGenreList(request, genre_id):
    genre = Genre.objects.get(id=genre_id)
    book_list = Book.objects.filter(genre_name=genre.genre_name)

    return render(
        request,
        'book/selected_genre.html',
        {
            'book_list': book_list,
            'genre_name': genre.genre_name
        }
    )


class BookList(ListView):
    model = Book
    template_name = 'book/book_list.html'


def bookDetail(request, book_isbn):
    user = request.user
    book = Book.objects.get(book_isbn=book_isbn)

    try:
        wishlist = WishBookList.objects.get(user_id=user, book_id=book)
        wished = True
    except:
        wished = False

    return render(
        request,
        'book/book_detail.html',
        {
            'book': book,
            'wishList': WishBookList,
            'wished': wished
        }
    )


def addWishList(request, book_isbn):
    user = request.user
    book = Book.objects.get(book_isbn=book_isbn)

    # 위시리스트 추가
    if request.POST.get('wish-cancle') == None:
        wish_book = WishBookList(user_id=user, book_id=book)
        WishBookList.save(wish_book)
        wished = True

    # 위시리스트 취소
    else:
        wish_list = WishBookList.objects.get(user_id=user, book_id=book)
        wish_list.delete()
        wished = False

    return render(
        request,
        'book/book_detail.html',
        {
            'book': book,
            'wished': wished
        }
    )


# def wishListView(request):
#     user = request.user
#     user_wishList = WishBookList.objects.filter(user_id=user)


#     return render(
#         request,
#         'profile/profile_wishList.html',
#         {
#             'wishList' : user_wishList
#         }
#     )

class WishList(ListView):
    model = Book
    ordering = '-pk'
    paginate_by = 5

    template_name = 'profile/profile_wishList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_id = self.kwargs.get('user_id')
        context['wishList'] = WishBookList.objects.filter(user_id=self.request.user)
        return context


# review
class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review/review_detail.html'
    pk_url_kwarg = 'review_id'


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'

    redirect_unauthenticated_users = True
    raise_exception = confirmation_required_redirect

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id": self.object.id})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review/review_form.html'
    pk_url_kwarg = 'review_id'

    raise_exception = True
    redirect_unauthenticated_users = False

    def get_success_url(self):
        return reverse("review-detail", kwargs={"review_id": self.object.id})

    def test_func(self, user):
        review = self.get_object()
        if review.author == user:
            return True
        else:
            return False


class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review/review_confirm_delete.html'
    pk_url_kwarg = 'review_id'

    raise_exception = True
    redirect_unauthenticated_users = False

    def get_success_url(self):
        return reverse('main')

    def test_func(self, user):
        review = self.get_object()
        if review.author == user:
            return True
        else:
            return False
