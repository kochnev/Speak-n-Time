from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from main.forms import LoginForm
# Create your views here.

def index(request):
    return render(request, 'main/index.html', {})

#def signin(request):
#    return render(request, 'main/signin.html', {})

def signin(request):
    message = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                message = 'username or password are incorrect'
    else:
        form = LoginForm()
    return render(request, 'main/signin.html',{
        'form': form,
        'message':message,
})

def signup(request):
        return render(request, 'main/signup.html', {})
