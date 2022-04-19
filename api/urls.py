from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from api.projects import views as api_projects_views
from api.users import views as api_users_views



urlpatterns = [
    path('projects/', api_projects_views.ReturnProjectsApiView.as_view(), name="projects_api"),
    path('projects/<str:pk>/', api_projects_views.ReturnProjectsApiView.as_view(), name="single_project_api"),
    path('projects/<str:pk>/vote/', api_projects_views.VoteProjectApiView.as_view(), name="vote_project_api"),

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register/', api_users_views.UserRegistrationApiView.as_view(), name="register_user_api"),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]