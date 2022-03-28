from django.shortcuts import render

# Create your views here.

def projects(request):
    return render(request, 'projects/projects.html')


def single_project(request):
    return render(request, 'projects/single-project.html')