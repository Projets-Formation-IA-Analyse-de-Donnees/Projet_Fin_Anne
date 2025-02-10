from django import forms
from .models import Projet_User

class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet_User
        fields = ['name','description']