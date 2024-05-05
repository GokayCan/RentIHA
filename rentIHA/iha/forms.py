from django import forms
from .models import IHA

# bu kısmı başta forumun otomatik oluşturulması için kullanıyordum sonradan gerek duymadım bu özelliğe
class IHAForm(forms.ModelForm):
    class Meta:
        model = IHA
        fields = ['brand', 'model', 'weight', 'category']