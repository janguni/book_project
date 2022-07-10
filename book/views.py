from multiprocessing import context
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login

from .forms import SignupForm
from django.views.generic import(
    DetailView, UpdateView, ListView, CreateView, DeleteView
)
from book.forms import ProfileForm, ReviewForm
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from book.models import User, Book, WishBookList, Review, Tag
from book.functions import confirmation_required_redirect


# with open('./bookList.csv','r',encoding="UTF-8") as f:
#     dr = csv.DictReader(f)
#     s = pd.DataFrame(dr)
# ss = []
# for i in range(len(s)):
#     st = (s['book_isbn'][i], s['book_img_url'][i], s['book_title'][i],s['book_author'][i],s['book_publisher'][i],s['genre_name'][i])
#     ss.append(st)
# for i in range(len(s)):
#     Book.objects.create(book_isbn=ss[i][0], book_img_url=ss[i][1], book_title=ss[i][2],book_author=ss[i][3],book_publisher=ss[i][4],genre_name=ss[i][5])


# main
def main(request):
    return render(request,'book/main.html')

# account/signup
def signup(request) : 
    if request.method == 'GET' :
        form = SignupForm()
   
    elif request.method == 'POST' :
        form = SignupForm(request.POST)
        if form.is_valid() :
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'account/signup_success.html')
    return render(request, 'account/signup.html', {'form': form})

# account/login    
def loginview(request) :
    if request.method == 'GET' :
            return render(request, 'account/login.html')

    elif request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None :
            login(request, user)
            # 로그인 성공
            return render(request, 'book/main.html')
        else :
            # 로그인 실패
            return render(request, 'account/login.html', {'error': '아이디 또는 비밀번호를 확인하세요!'})
    else : 
        return render(request, 'account/login.html')

# profile
class ProfileView(DetailView):
    model = User
    template_name = 'profile/profile.html'
    pk_url_kwarg = 'user_id'
    context_object_name = 'profile_user'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id')
       
        return context

class ProfileSetView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile/profile_set_form.html'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self) :
        return reverse('main')

class ProfileUpdateView(LoginRequiredMixin,UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'profile/profile_update_form.html'

    def get_object(self, queryset= None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('profile',kwargs=({'user_id':self.request.user.id}))

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView) :
    def get_success_url(self):
        return reverse('profile',kwargs=({'user_id':self.request.user.id})) 

# 검색 기능
def search(request) :
    if request.method == "GET":
        search_key = request.GET['q']
        option_select = request.GET.getlist('option_select',None)
        
        if 'all' in option_select :
            search_books = Book.objects.filter(Q(book_title__icontains = search_key) | Q(book_publisher__icontains = search_key) | Q(book_author__icontains = search_key) | Q(genre_name__icontains = search_key))

        elif 'title' in option_select :
            search_books = Book.objects.filter(Q(book_title__icontains = search_key))

        elif 'author' in option_select :
            search_books = Book.objects.filter(Q(book_author__icontains = search_key))

        elif 'publisher' in option_select :
            search_books = Book.objects.filter(Q(book_publisher__icontains = search_key))

        elif 'genre' in option_select :
            search_books = Book.objects.filter(Q(genre_name__icontains = search_key))

        return render(request,'book/search.html', {'search_books': search_books, 'search_key': search_key})
    
    else:
        return render(request, 'book/main.html')


class BookList(ListView):
    model = Book
    template_name = 'book/book_list.html'


def bookDetail(request,book_isbn):
    user = request.user
    book = Book.objects.get(book_isbn=book_isbn)

    try:
        wishlist = WishBookList.objects.get(user_id=user,book_id=book) 
        wished=True
    except:
        wished=False


    return render(
        request,
        'book/book_detail.html',
        {
            'book': book,
            'wishList': WishBookList,
            'wished' : wished
        }
    )


def addWishList(request, book_isbn):
    user = request.user
    book = Book.objects.get(book_isbn=book_isbn)

    # 위시리스트 추가
    if request.POST.get('wish-cancle') == None:
        wish_book = WishBookList(user_id=user, book_id=book)
        WishBookList.save(wish_book)
        wished=True

    # 위시리스트 취소
    else:
        wish_list = WishBookList.objects.get(user_id=user, book_id=book)
        wish_list.delete()
        wished=False

    
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
        #user_id = self.kwargs.get('user_id')
        context['wishList'] = WishBookList.objects.filter(user_id=self.request.user)
        return context
