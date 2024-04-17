# forms.py
from django import forms
from django.apps import apps
from invent_app.models import CustomUser

def generate_dynamic_model_forms():
    dynamic_forms = {}
    models = apps.get_models()
    for model in models:
        Meta = type('Meta', (object,), {'model': model, 'fields': '__all__'})
        form_class = type(f'{model.__name__}Form', (forms.ModelForm,), {'Meta': Meta})
        dynamic_forms[model.__name__] = form_class
    return dynamic_forms

from .models import Feedback, Location, SubLocations, FeedbackCategory, Department,FarmerFeedback


class FeedbackForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), empty_label="Select Location", required=True, 
                                      widget=forms.Select(attrs={'class': 'custom-select'}))
    class Meta:
        model = Feedback
        fields = [ 'mobile', 'sub_location', 'message','feedback_cat', 'file']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'sub_location': forms.Select(attrs={'class': 'custom-select'}),
            'feedback_cat': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class MemberFeedbackForm(forms.ModelForm):
    file = forms.FileField(required=False)
    class Meta:
        model = FarmerFeedback
        fields = ['name', 'mobile', 'mpp', 'district','message', 'file']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 2,'class':'form-control'}),
        }

class ForwardFeedbackForm(forms.Form):
    
    hods = forms.ModelChoiceField(queryset=CustomUser.objects.none(), empty_label="Select HOD", required=True, 
                                      widget=forms.Select(attrs={'class': 'custom-select'}))

    def __init__(self, *args, role=None, **kwargs):
        super().__init__(*args, **kwargs)
        if role:
            self.fields['hods'].queryset = CustomUser.objects.filter(role=role)

class CloseFeedbackForm(forms.Form):
    remark = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control','rows': 2}))


from django import forms
from .models import Profile, CustomUser

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'dob', 'gender', 'profile_image']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import CustomUser, Profile

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=100, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['phone_number', 'dob', 'gender', 'profile_image']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
