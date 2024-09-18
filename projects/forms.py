# Django imports
from django import forms
# Local imports
from .models import Project, Review
# Third party imports
from cloudinary.forms import CloudinaryFileField


class ProjectForm(forms.ModelForm):
    featured_image = CloudinaryFileField(options={'tags': 'project-image', 'format': 'png'})
    
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {'value': 'Submit your vote', 'body': 'Submit a review (optional)'}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text', 'id': f'formInput{label.capitalize()}'})