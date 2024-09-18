# Django imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
# Local imports
from .models import Profile, Skill, Message
# Third party imports
from cloudinary.forms import CloudinaryFileField


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class ProfileForm(ModelForm):
    profile_image = CloudinaryFileField(options={'tags': 'profile-image', 'format': 'png'})
    
    class Meta:
        model = Profile
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs.update({'id': f'formInput{label.capitalize()}', 'class': 'input input--text'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs.update({'id': f'formInput{label.capitalize()}', 'class': 'input input--text'})


class SendMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super(SendMessageForm, self).__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs.update({'id': f'formInput{label.capitalize()}','class': 'input input--text'})