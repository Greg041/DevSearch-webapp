from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Profile


def search_profiles(request):
    query = request.GET.get('search')
    profiles_by_name_intro = Profile.objects.filter(Q(name__icontains=query) | Q(short_intro__icontains=query)).distinct().exclude(profile_image='').annotate(projects_number=Count('project')).order_by('-projects_number')
    if not profiles_by_name_intro:
        profiles_by_skills = Profile.objects.get_profiles_by_skills(query).exclude(profile_image='').annotate(projects_number=Count('project')).order_by('-projects_number')
        return profiles_by_skills, query
    else:
        return profiles_by_name_intro, query

    
def paginate_profiles(request, projects_queryset, number_profiles_per_page):
    profiles_paginator = Paginator(projects_queryset, number_profiles_per_page)
    page_number = request.GET.get('page')
    try:
        profiles = profiles_paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        profiles = profiles_paginator.page(page_number)
    except EmptyPage:
        page_number = profiles_paginator.num_pages
        profiles = profiles_paginator.page(page_number)
    
    left_index = int(page_number) - 1
    if left_index < 1:
        left_index = 1
    right_index = int(page_number) + 2
    if right_index > profiles_paginator.num_pages:
        right_index = profiles_paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return profiles, custom_range