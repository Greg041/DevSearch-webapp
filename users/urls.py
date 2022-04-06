from django.urls import path
from . import views


urlpatterns = [
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name='user_profile'),
    path('login/', views.login_user, name='login_page'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('my-account/', views.user_account, name='my_account'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('add-skill/', views.add_skill, name='add_skill'),
    path('edit-skill/<str:pk>', views.edit_skill, name='edit_skill'),
    path('delete-skill/<str:pk>', views.delete_skill, name='delete_skill'),
    path('inbox', views.inbox, name='inbox'),
    path('read-message/<str:pk>', views.read_message, name='read_message')
]