from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import include
from api.projects import views as api_projects_views
from api.users import views as api_users_views



urlpatterns = [
    path('projects/', api_projects_views.ProjectsApiView.as_view(), name="projects_api"),
    path('projects/<str:pk>/', api_projects_views.ProjectCrudApiView.as_view(), name="project_crud_api"),
    path('projects/<str:pk>/review/', api_projects_views.ReviewProjectApiView.as_view(), name="review_project_api"),
    path('projects/<str:pk>/review/<str:id>/', api_projects_views.UpdateReviewProjectView.as_view(), name="update_review_project_api"),

    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register/', api_users_views.UserRegistrationApiView.as_view(), name="register_user_api"),
    path('users/logout/', api_users_views.LogoutApiView.as_view(), name='logout_api'),
    path('users/password-reset/', include('django_rest_passwordreset.urls', namespace="password_reset")),

    path('profiles/', api_users_views.ListProfilesApiView.as_view(), name='profiles_api'),  # Used only to return profiles list, the creation of a profile is made automatically when a user is registered
    path('profiles/<str:pk>/', api_users_views.ProfileApiView.as_view(), name='single_profile_api'),
    path('profiles/<str:pk>/skills/', api_users_views.ProfileSkillsApiView.as_view(), name="profile_skills_api"),  # Return and create skills of the authenticated profile
    path('profiles/<str:pk>/skills/<str:id>/', api_users_views.ProfileSkillRUDApiView.as_view(), name="profile_skill_rud_api"),
    path('profiles/<str:pk>/messages/', api_users_views.MessagesApiView.as_view(), name="profile_messages_api"),
    path('profiles/<str:pk>/messages/<str:id>', api_users_views.SingleMessageApiView.as_view(), name="profile_single_message_api"),
    path('sent-message/<str:pk>/', api_users_views.SendMessageApiView.as_view(), name="sent_message_api"),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger_ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
]