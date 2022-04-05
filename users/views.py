from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.aggregates import Count
from .utils import search_profiles, paginate_profiles
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm


# Create your views here.
def profiles(request):
    if request.GET.get('search'):
        profiles, query = search_profiles(request)
    else:
        query = ''
        profiles = Profile.objects.all().annotate(projects_number=Count('project')).order_by('-projects_number')
    profiles, custom_range = paginate_profiles(request, profiles, 3)
    context = {
        'profiles': profiles,
        'query': query,
        'pagination_range': custom_range
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
                return redirect('my_account')
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
        return redirect('my_account')

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


@login_required(login_url='login_page')
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = request.user.profile
            skill.name = skill.name.capitalize()
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('my_account')
        else:
            context = {
                'form': form
            }
            messages.error("There was an error adding your skill, please try again")
            return render(request, 'users/add-skill-form.html', context)
    else:
        form = SkillForm()
        context = {
            'form': form
        }
        return render(request, 'users/add-skill-form.html', context)


@login_required(login_url='login_page')
def edit_skill(request, pk):
    skill = Skill.objects.filter(id=pk).first()
    if skill.owner == request.user.profile:
        if request.method == 'POST':
            form = SkillForm(request.POST, instance=skill)
            if form.is_valid():
                skill = form.save(commit=False)
                skill.owner = request.user.profile
                skill.save()
                messages.success(request, "Skill was updated successfully!")
                return redirect('my_account')
            else:
                context = {
                    'form': form
                }
                messages.error(request, "There was an error updating your skill, please try again")
                return render(request, 'users/add-skill-form.html', context)
        else:
            form = SkillForm(instance=skill)
            context = {
                'form': form
            }
            return render(request, 'users/add-skill-form.html', context)
    else:
        return redirect('my_account')


@login_required(login_url='login_page')
def delete_skill(request, pk):
    skill = Skill.objects.filter(id=pk).first()
    if skill.owner == request.user.profile:
        if request.method == 'POST':
            skill.delete()
            messages.success(request, "The skill was deleted successfully")
            return redirect('my_account')
        else:
            context = {
                'object': skill
            }
            return render(request, 'delete-template.html', context)