from django.forms import ModelForm
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        
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