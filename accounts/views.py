from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.models import User
from .forms import ProfileForm
from accounts.forms import UserLoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
import json

# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect(reverse('index'))
    
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
                                    
            
            if user:
                auth.login(user=user, request=request)
                messages.success(request, 'You have successfully logged in.')
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, 'Your username or password is incorrect.')
    else:
        login_form = UserLoginForm()
    return render(request, 'login.html', {'login_form': login_form})
    
def registration(request):
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        print('before is valid reg')
        if registration_form.is_valid():
            registration_form.save()
             
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password1'] )
            print('before is user reg')
            if user:
                auth.login(user=user, request=request)
                messages.success(request, 'You have successfully registered')
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register your account at this time.')
    else:
        registration_form = UserRegistrationForm()
    return render(request, 'registration.html', {'registration_form': registration_form})

@login_required  
def user_profile(request):
    print('HAVE ARRIVED HERE')
    user = User.objects.get(pk=request.user.id)
    print('USER before post', user.profile.avatar_url)
    
    if request.method == 'POST':
        print('NOW IN POST SECTION')
        user = User.objects.get(pk=request.user.id)
        avatar_url = request.POST.get('avatar_url')
        print('URL',avatar_url)
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print('FORM IS VALID')
            user.profile.avatar_url=avatar_url
            user.save()
            print('USER', user.profile.avatar_url)
        
        form = ProfileForm()
        return render(request, 'profile.html', {'profile': user, 'form': form})
    else:
        user = User.objects.get(email=request.user.email)
        print(user.profile.avatar_url)
        form = ProfileForm()
        
        return render(request, 'profile.html', {'profile': user, 'form': form})
    
    
def add_avatar(request):
    
    if request.method == 'POST':
        response_data = {}
        
        user = User.objects.get(pk=request.user.id)
        avatar_url = request.POST.get('author_url')
        print('URL',avatar_url)
        print(user.username)
        #user.profile.avatar_url = avatar_url
        form = ProfileForm(request.POST, request.FILES, instance=user)
        form.save()
        print('After save',user.profile.avatar_url)
        
        return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )