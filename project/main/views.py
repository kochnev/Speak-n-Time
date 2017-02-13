from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login

from main.forms import UserForm, UserProfileForm
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


# Create your views here.
def register(request):
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
             print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'main/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})
