from django.urls import reverse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .forms import SignupForm
from django.views.generic import(
    DetailView,UpdateView
)
from book.forms import ProfileForm
from braces.views import LoginRequiredMixin
from allauth.account.views import PasswordChangeView
from book.models import User

# main
def main(request):
    return render(request,'book/main.html')

# account
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

        # username = request.POST.get('username', None)
        # password = request.POST.get('password', None)
        # re_password = request.POST.get('re_password', None)
        # email = request.POST.get('email', None)
        # nickname = request.POST.get('nickname', None)

        # res_data={}

        # if not(username and password and re_password and email and nickname) :
        #     res_data['error'] = "모든 값을 입력해야 합니다."

        # elif password != re_password :
        #     res_data['error'] = "비밀번호가 다릅니다!"
        # else :
        #     form = CustomUser (
        #         username = username,
        #         password = make_password(password),
        #         email = email,
        #         nickname = nickname,
        #     )
        #     form.save()
        #     return render(request, 'common/signup_success.html')
        # return render(request, 'common/signup.html',res_data)

     
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
            return render(request, 'account/login.html', {'error': '아이디 혹은 패스워드가 올바르지 않습니다.'})
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