from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.

def profiles(request):
    profiles, search_query = searchProfiles(request)
    
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    context = {'profiles': profiles, 'search_query': search_query, 'custom_range': custom_range}
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
    profile = request.user.profile
    form = SkillForm()
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request, "Skill was successfully updated!")
            return redirect('account')
    
    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "Skill was successfully deleted!")
        return redirect('account')
    
    # using object because several things can be deleted through the delete_template and we are using the variable object in that html file
    context = {'object': skill}
    return render(request, 'delete_template.html', context)