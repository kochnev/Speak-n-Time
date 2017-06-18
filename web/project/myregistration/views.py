from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, UserProfileForm

# Create your views here.
def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to # True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information. # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        #profile_form = UserProfileForm(data=request.POST)
        # If the two forms are valid...
        if user_form.is_valid(): #and profile_form.is_valid():  # Save the user's form data to the database.
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            #profile = profile_form.save(commit=False)
            #profile.user = user

            #if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']  # Now we save the UserProfile model instance.

            #profile.save()

            registered = True
        else:
            print(user_form.errors)#, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        #  These forms will be blank, ready for user input.
        user_form = UserForm()
        #profile_form = UserProfileForm()
        # Render the template depending on the context.

    return render(request, 'myregistration/registration_form.html',
                      {'form': user_form,
                       #'profile_form': profile_form,
                       'registered': registered})


def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)

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
                return redirect('index')
            else:
                return HttpResponse("Your Speak-n-time account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            #return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'myregistration/login.html', {})

def user_logout(request):
    logout(request)
    return redirect('index')
