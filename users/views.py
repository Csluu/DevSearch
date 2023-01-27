from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm

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
        username = request.POST['username'].lower()
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
            return redirect('edit-account')
        else:
            messages.success(request, 'Error has occurred during registration!')
    
    
    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

@login_required(login_url='login')
def userAccount(request):
    # request.user is the current user
    profile = request.user.profile
    
    skills = profile.skill_set.all()
    
    context = {'profile': profile, 'skills': skills}
    
    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # need to do instance=profile to preload the information
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        # request.POST is normally text data, request.FILE is the picture
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            return redirect('account')
    
    
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    form = SkillForm()
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)