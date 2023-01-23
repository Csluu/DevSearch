from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Review, Tag
from .forms import ProjectForm

# Create your views here.

def projects(request):
    projects = Project.objects.all()
    context = {'projects': projects}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context = {'project': projectObj}
    return render(request, 'projects/single-projects.html', context)

def createProject(request):
    form = ProjectForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            # send user back to projects page. Remember we get 'projects' from urls.py
            return redirect('projects')
    
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            # send user back to projects page. Remember we get 'projects' from urls.py
            return redirect('projects')
    
    context = {'form': form}
    return render(request, "projects/project_form.html", context)

def deleteProject(request, pk):
    # we are using objects so that we are able to delete anything, parent, and children of Project?
    project = Project.objects.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {'object': project}
    return render(request, "projects/delete_template.html")