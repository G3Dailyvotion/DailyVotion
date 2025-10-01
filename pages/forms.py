from django import forms
from .models import JournalEntry, PrayerRequest, Reflection, Feedback, UserProfile
from django.contrib.auth.models import User


class JournalEntryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = JournalEntry
        fields = ['date', 'scripture', 'observation', 'application', 'prayer']


class ProfileForm(forms.ModelForm):
    # Fields for User model that we'll handle manually
    full_name = forms.CharField(max_length=60, required=False, 
                              widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    username = forms.CharField(max_length=30, required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    
    class Meta:
        model = UserProfile
        fields = ['image', 'bio']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
        }


class PrayerRequestForm(forms.ModelForm):
    class Meta:
        model = PrayerRequest
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your prayer request here...'})
        }


class ReflectionForm(forms.ModelForm):
    class Meta:
        model = Reflection
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'placeholder': "Type your reflection here..."})
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your feedback or report here...'})
        }
