from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag


def search_projects(request):
    query = request.GET.get('search')
    tags = Tag.objects.filter(name__icontains=query)
    projects = Project.objects.distinct().filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(owner__name__icontains=query) | Q(tags__in=tags)).order_by('-created')
    return projects, query 


"""Works for paginate the queryset recieved and returns the queryset slice object
for the actual page and the range of pages visibles to select in pagination navigation menu"""
def paginate_projects(request, projects_queryset, number_projects_per_page):
    projects_paginator = Paginator(projects_queryset, number_projects_per_page)
    page_number = request.GET.get('page')
    try:
        projects = projects_paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        projects = projects_paginator.page(page_number)
    except EmptyPage:
        page_number = projects_paginator.num_pages
        projects = projects_paginator.page(page_number)
    
    left_index = int(page_number) - 1
    if left_index < 1:
        left_index = 1
    right_index = int(page_number) + 2
    if right_index > projects_paginator.num_pages:
        right_index = projects_paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return projects, custom_range