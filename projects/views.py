from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project, Review
from .forms import ProjectForm
# Create your views here.

def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {
        'projects': projects,
    })


def single_project(request, pk):
    project = Project.objects.filter(id=pk).first()
    return render(request, 'projects/single-project.html', {
        'project': project,
    })


@login_required(login_url='login_page')
def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user.profile
            project.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login_page')
def update_project(request, pk):
    if request.user == project.owner.user:
        project = Project.objects.filter(id=pk).first()
        form = ProjectForm(instance=project)
        if request.method == 'POST':
            form = ProjectForm(request.POST, request.FILES, instance=project)
            if form.is_valid():
                form.save()
                return redirect('projects')
        context = {'form': form}
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
        return render(request, 'projects/delete-template.html', context)
    else:
        return redirect('my_account')