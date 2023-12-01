# projectName/forms.py

from django import forms
from .models import File, DocumentTask

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['file','folder']

class DocumentTaskForm(forms.ModelForm):
    class Meta:
        model = DocumentTask
        fields = ['receiver', 'file', 'task_description']
