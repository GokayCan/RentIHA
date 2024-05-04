from django import forms
from .models import IHA

class IHAForm(forms.ModelForm):
    class Meta:
        model = IHA
        fields = ['brand', 'model', 'weight', 'category']