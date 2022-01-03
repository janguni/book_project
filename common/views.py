from django.shortcuts import render
from django.contrib.auth import authenticate, login

def login(request) :
    if request.method == 'GET' :
        return render(request, 'common/login.html')

    elif request.method == 'POST' :
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None :
            login(request, user)
            # Redirect to a success page.
            return redirect('commom/login.html')
        else :
            # Return an 'invalid login' error message
            return render(request, 'login.html', {'error': 'username or password is incorrect'})
    else : 
        return render(request, 'common/login.html')