from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    
    #  for pagination 
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
    
    try:
        projects = paginator.page(page)
    # if theres no search query/page number at the time the default page will be 1
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    # basically if a user manually types in a page number on the top more than the available max pages just send the user to the last available page
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    
    # we are setting it up so it doesn't display like 1000 page buttons on the bottom 
    leftIndex = (int(page)-4)
    
    if leftIndex <1:
        leftIndex = 1
        
    rightIndex = (int(page)+5)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1
        
    custom_range = range(leftIndex, rightIndex)
    
    return custom_range, projects


def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)

    # using __ in owner__name__icontains to go up to the parent model and grabbing the name attribute 
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
    )
    
    return projects, search_query