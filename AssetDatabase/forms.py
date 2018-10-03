from django import forms
from django.forms import ModelForm
from . import models
from .models import Building


class AssetForm(forms.ModelForm):
    def __str__(self):
        return self.asset_name

    class Meta:
        model = models.Asset
        fields = ('location', 'name', 'room', 'image', 'optional_field',)
        
class AdministrationForm(forms.ModelForm):
    def __str__(self):
        return self.building_name
    
    class Meta:
        model = Building
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(label='User Name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())
