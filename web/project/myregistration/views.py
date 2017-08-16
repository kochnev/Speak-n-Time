from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone
from .forms import UserForm, UserProfileForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('register_profile')
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        #  These forms will be blank, ready for user input.
        user_form = UserForm()
    return render(request, 'myregistration/registration_form.html',
                      {'form': user_form,})


def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            if 'picture' in request.FILES:
                user_profile.picture = request.FILES['picture']
            user_profile.save()
            return redirect('index')

    context_dict = {'form':form}

    return render(request, 'myregistration/registration_profile.html', context_dict)

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                user.profile.last_login = timezone.now()
                return redirect('index')
            else:

                messages.add_message(request, messages.ERROR, 'Пользователь заблокирован!')
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Неверно введен логин или пароль!')
            return redirect('login')
    else:
        return render(request, 'myregistration/login.html', {})

def user_logout(request):
    logout(request)
    return redirect('index')
