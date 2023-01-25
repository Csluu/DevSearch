from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill
from .forms import CustomUserCreationForm

# Create your views here.

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

def loginUser(request):
    
    # determines if the page is going to be login or register
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profiles')
    
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # I feel like this section could definitely be written better [------------
        try:
            # trying to see if its a valid user 
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username does not exist")
        
        # tries to make sure that the password matches the username
        user = authenticate(request, username=username, password=password)
        
        # logins the user in 
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is incorrect')
        # -------------------------------------------------------------------------]
        
    return render(request, 'users/login_register.html')

def logoutUser(request):
    # deletes user session in the browser
    messages.info(request, "User has logged out")
    logout(request)
    return redirect('login')

def registerUser(request):
    # determines if the page is going to be login or register
    page = 'register'
    form = CustomUserCreationForm()
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            messages.success(request, 'User account was created!')
            
            login(request, user)
            return redirect('profiles')
        else:
            messages.success(request, 'Error has occurred during registration!')
    
    
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)