from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Project, Review, Tag
from .forms import ProjectForm
from .utils import searchProjects, paginateProjects

# Create your views here.

def projects(request):
    projects, search_query = searchProjects(request)
    
    custom_range, projects  = paginateProjects(request, projects, 6)
    
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {'project': projectObj}
    return render(request, 'projects/single-projects.html', context)

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            # send user back to projects page. Remember we get 'projects' from urls.py
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
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            # send user back to projects page. Remember we get 'projects' from urls.py
            return redirect('account')
    
    context = {'form': form}
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
    return render(request, "delete_template.html")