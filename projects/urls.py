from django.urls import path
from .views import projects, single_project

urlpatterns = [
    path('', projects, name="projects"),
    path('projects/<int:pk>', single_project, name=single_project)
]