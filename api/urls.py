from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from api.projects import views


urlpatterns = [
    path('projects/', views.projects_api_view, name="projects_api"),
    path('projects/<int:pk>', views.single_project_api_view, name="single_project_api"),
    path('projects/<int:pk>/vote', views.vote_and_review_project_api_view, name="vote_project_api"),
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]