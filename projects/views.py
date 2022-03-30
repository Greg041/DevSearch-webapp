from django.shortcuts import render, redirect
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


def create_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('projects ')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


def update_project(request, pk):
    project = Project.objects.filter(id=pk).first()
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


def delete_project(request, pk):
    project = Project.objects.filter(id=pk).first()
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {
        'object': project
    }
    return render(request, 'projects/delete-template.html', context)