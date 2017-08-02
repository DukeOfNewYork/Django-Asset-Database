from django import forms
from django.forms import ModelForm
from . import models
from .models import Building

class AssetForm(forms.ModelForm):
    def __str__(self):
        return self.asset_name
    class Meta:
        model = models.Asset
        fields = ('location','name','room','image')
