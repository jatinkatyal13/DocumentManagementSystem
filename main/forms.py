from django import forms
from main import models

class FileForm(forms.ModelForm):
    url = forms.FileField(required=False)
    markdown = forms.CharField(required=False)
    docType = forms.CharField(required=True)
   
    class Meta:
        model = models.File
        fields = ['name', 'readFlag', 'writeFlag']
