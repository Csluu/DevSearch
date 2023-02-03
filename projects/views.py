from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Review, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

# Create your views here.

def projects(request):
    projects, search_query = searchProjects(request)
    
    custom_range, projects  = paginateProjects(request, projects, 6)
    
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method =='POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        
        # updating votes
        # @property allows us to run it like this 
        projectObj.getVoteCount
        
        messages.success(request, 'Your review was successfully submitted!')
        # redirects to the same page so that the review information isn't there when you submit it 
        return redirect('project', pk=projectObj.id)
    
    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-projects.html', context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
    # making sure only the user who created the project can edit 
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        # adding new tags
        newtags = request.POST.get('newtags').replace(',', " ").split()
        
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                # if the tag isn't created it will get the tag instead
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            # send user back to projects page. Remember we get 'projects' from urls.py
            return redirect('account')
    
    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def deleteProject(request, pk):
    # we are using objects so that we are able to delete anything, parent, and children of Project?
    # project = Project.objects.get(id=pk)
    
    #     # making sure only the user who created the project can delete
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    
    
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {'object': project}
    return render(request, "delete_template.html", context)