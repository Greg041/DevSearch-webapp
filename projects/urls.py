from django.urls import path
from .views import projects, single_project, create_project, update_project, delete_project

urlpatterns = [
    path('', projects, name="projects"),
    path('projects/<str:pk>', single_project, name="single_project"),
    path('create-project/', create_project, name="create_project"),
    path('update-project/<str:pk>/', update_project, name="update_project"),
    path('delete-project/<str:pk>', delete_project, name="delete_project")
]