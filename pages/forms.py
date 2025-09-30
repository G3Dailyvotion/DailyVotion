from django import forms
from .models import JournalEntry, PrayerRequest, Reflection, Feedback


class JournalEntryForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = JournalEntry
        fields = ['date', 'scripture', 'observation', 'application', 'prayer']


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
