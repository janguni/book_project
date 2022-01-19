from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import SignupForm

def main(request) :
    return render(request, 'common/main.html')

def signup(request) : 
    if request.method == 'GET' :
        form = SignupForm()
        return render(request, 'common/signup.html', {'form': form})
   
    elif request.method == 'POST' :
        form  = SignupForm(request.POST)

        if form.is_valid() :
            form.signup()
            return render(request, 'common/signup_success.html')
        return render(request, 'common/signup.html')

     
def login(request) :
    if request.method == 'GET' :
        return render(request, 'common/login.html')

    elif request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None :
            login(request, user)
            # 로그인 성공
            return redirect('commom/login.html')
        else :
            # 로그인 실패
            return render(request, 'login.html', {'error': '아이디 혹은 패스워드가 올바르지 않습니다.'})
    else : 
        return render(request, 'common/login.html')

