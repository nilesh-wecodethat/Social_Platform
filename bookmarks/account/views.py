from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from account.forms import LoginForm
from django.contrib.auth.decorators import login_required


def user_login(request) : 
    if request.method == 'POST':
       form = LoginForm(request.POST)

       if form.is_valid() :
            data = form.cleaned_data
            user = authenticate(request,
                               username= data['username'],
                               password = data['password'])

            if user is not None :
                if user.is_active:
                    login(request, user)

                    return HttpResponse('Authenticated Successfully')
                else : 
                    return HttpResponse("Disabled Account")
            
            else:
                return HttpResponse("Auth Failed")
    
    else:
        form = LoginForm()
    
    return render(request, 'account/login.html' , {'form' : form})



@login_required
def dashboard(request) : 
    return render(request, 
            'account/dashboard.html',
            {'section' : 'dashboard'})