from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_projects, paginate_projects


def projects(request):
    if request.GET.get('search'):
        projects, query = search_projects(request)
    else:
        query = ''
        projects = Project.objects.exclude(featured_image='')
        
    projects, custom_range = paginate_projects(request, projects, 3)
    context = {
        'projects': projects,
        'query': query,
        'pagination_range': custom_range
    }
    return render(request, 'projects/projects.html', context)


def single_project(request, pk):
    project = Project.objects.filter(id=pk).first()
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.owner = request.user.profile
            review.project = project
            review.save()
            project.get_votes_total
            messages.success(request, 'Your review has been successfully submitted')
            redirect('single_project', pk=project.id)
        else:
            context = {
                'project': project,
                'review_form': review_form
            }
            render(request, 'projects/single-project.html', context)
    review_form = ReviewForm()
    context = {
        'project': project,
        'review_form': review_form
    }
    return render(request, 'projects/single-project.html', context)
 

@login_required(login_url='login_page')
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            tags = Tag.objects.filter(name__in=request.POST.keys())
            project.tags.add(*tags)
            return redirect('projects')
    user_skills = request.user.profile.skill_set.all().values_list('name', flat=True)
    tags_available = Tag.objects.filter(name__in=user_skills)
    context = {
        'form': form,
        'tags': tags_available
        }
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login_page')
def update_project(request, pk): 
    project = Project.objects.filter(id=pk).first()
    if request.user == project.owner.user:
        form = ProjectForm(instance=project)
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                project.tags.clear()
                tags = Tag.objects.filter(name__in=request.POST.keys())
                project.tags.add(*tags)
                return redirect('my_account')
        user_skills = request.user.profile.skill_set.all().values_list('name', flat=True)
        tags_available = Tag.objects.filter(name__in=user_skills)
        context = {
            'project': project,
            'form': form,
            'tags': tags_available
            }
        return render(request, 'projects/project-form.html', context)
    else:
        return redirect('my_account')


@login_required(login_url='login_page')
def delete_project(request, pk):
    project = Project.objects.filter(id=pk).first()
    if request.method == 'POST':
        if request.user == project.owner.user:
            project.delete()
            return redirect('projects')
    if request.user == project.owner.user:
        context = {
            'object': project
        }
        return render(request, 'delete-template.html', context)
    else:
        return redirect('my_account')