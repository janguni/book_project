from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def main(request) :
    return render(request, 'common/main.html')

def signup(request) :
    if request.method == 'GET'
        return render(request, 'common/signup.html')

    elif request.method == 'POST' :
        username = request.POST('username')
        password = request.POST('password')
        password2 = request.POST('password2')
        print(username, password, password2)
        user = User()
        user.username = username
        user.password = password
        user.save()
        return render(request, 'common/signup_success.html')

    else :
        context_values = {'form':'This is form'}
        return render(request, 'common/signup.html', context_values)

       
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

