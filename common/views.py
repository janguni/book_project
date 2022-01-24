from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from .forms import SignupForm
from .models import CustomUser


def main(request) :
    return render(request, 'common/main.html')

def signup(request) : 
    if request.method == 'GET' :
        form = SignupForm()
   
    elif request.method == 'POST' :
        form = SignupForm(request.POST)
        if form.is_valid() :
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'common/signup_success.html')
    return render(request, 'common/signup.html', {'form': form})

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
        return render(request, 'common/login.html')

    elif request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None :
            login(request, user)
            # 로그인 성공
            return render(request, 'common/main.html')
        else :
            # 로그인 실패
            return render(request, 'login.html', {'error': '아이디 혹은 패스워드가 올바르지 않습니다.'})
    else : 
        return render(request, 'common/login.html')

