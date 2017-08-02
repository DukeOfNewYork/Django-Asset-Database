from django.db import models
from django.forms import ModelForm
from django import forms

# Create your models here.


class Building(models.Model):
    name = models.CharField(max_length=100)    
    def __str__(self):
        return (self.name)
 
class Asset(models.Model):
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Building, related_name='Asset')
    room = models.CharField(max_length=100)
    pub_date = models.DateTimeField('%Y-%m-%d %H:%M:%S', auto_now=True)
    image = models.ImageField(upload_to='asset_images',default='default.png',blank=True)
    def __str__(self):
        return (self.name + " " + self.location.name )
