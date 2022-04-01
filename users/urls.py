from django.urls import path
from . import views


urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name='user_profile'),
    path('login/', views.login_user, name='login_page'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('my-account/', views.user_account, name='my_account'),
    path('edit-profile/', views.edit_profile, name='edit_profile')
]