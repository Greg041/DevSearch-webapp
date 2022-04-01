from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm


# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles': profiles
    }
    return render(request, 'users/profiles.html', context)


def user_profile(request, pk):
    profile = Profile.objects.filter(id=pk).first()
    main_skills = profile.skill_set.exclude(description="")
    other_skills = profile.skill_set.filter(description="")
    context = {
        'profile': profile,
        'main_skills': main_skills,
        'other_skills': other_skills
    }
    return render(request, "users/user-profile.html", context)


def login_user(request):
    
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username__iexact=username).first()
        if user:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profiles')
            else:
                messages.error(request, "Username or password incorrect")
        else:
             messages.error(request, "User doesn't exist")

    context = {
        'page': 'login'
    }
    return render(request, "users/login-register.html", context)


def logout_user(request):
    logout(request)
    messages.info(request, "User was logged out")
    return redirect('login_page')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "Your account was successfully created!")
            login(request, user)
            return redirect('my_account')
        else:
            context = {
                'page': 'register',
                'form': form
            }
            messages.error(request, "There was an error when registering the user, check all fields are filled correctly")
            return render(request, 'users/login-register.html', context)
    else:
        context = {
            'page': 'register',
            'form': CustomUserCreationForm()
        }
        return render(request, 'users/login-register.html', context)


@login_required(login_url='login_page')
def user_account(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login_page')
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('my_account')
    form = ProfileForm(instance=request.user.profile)
    context = {
        'form': form
    }
    return render(request, 'users/profile-form.html', context)