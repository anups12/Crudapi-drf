from django import forms
from . models import Course
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CreatorRegister(UserCreationForm):
    class Meta:
        model = User
        fields=('username', 'email', 'password1', 'password2')
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Unique username'}),
            'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password '}),
            'password2':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}),
        }

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'image', 'description','title')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name of Course'}),
            'description':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description of course', 'wrap':'off', 'rows':6}),
            'title':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'image':forms.FileInput(attrs={'class':'form-control'}),
        }