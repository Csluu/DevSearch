from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link',]
        
        widgets ={
            'tags':forms.CheckboxSelectMultiple(),
        }
        
    def __init__(self, *args, **kwargs):
        # reminder its inheriting from ProjectForm
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
            
        # to do it individually
        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder': 'Add title'})
        
class ReviewForm(ModelForm):
    class Meta: 
        model = Review
        fields = ['value', 'body']
        
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
        }
        
    def __init__(self, *args, **kwargs):
        # reminder its inheriting from ProjectForm
        super(ReviewForm, self).__init__(*args, **kwargs)
    
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})