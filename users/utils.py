from .models import Profile, Skill
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    
    #  for pagination 
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)
    
    try:
        profiles = paginator.page(page)
    # if theres no search query/page number at the time the default page will be 1
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # basically if a user manually types in a page number on the top more than the available max pages just send the user to the last available page
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)
    
    # we are setting it up so it doesn't display like 1000 page buttons on the bottom 
    leftIndex = (int(page)-4)
    
    if leftIndex <1:
        leftIndex = 1
        
    rightIndex = (int(page)+5)
    
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages +1
        
    custom_range = range(leftIndex, rightIndex)
    
    return custom_range, profiles



def searchProfiles(request):
    search_query = ''
    
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    print('SEARCH:', search_query)
    
    skills = Skill.objects.filter(name__icontains=search_query)
    
    # Profile.objects.filter(name__icontains=search_query, short_intro__icontains=search_query) 
    # Having it like this requires both name and short_bio to contain the same string - that is why we use Q look up for either one (OR)
    # with using Q look up can use & or | when searching for more than one parameter 
    # using skill__in to filter child objects of the profile parent model
    # have to use distinct or else skills filter will bring in several profiles
    profiles = Profile.objects.distinct().filter(Q(name__icontains=search_query) | Q(short_intro__icontains=search_query) | Q(skill__in=skills))
    return profiles, search_query