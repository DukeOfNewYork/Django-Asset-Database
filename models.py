from django.db import models
from django.contrib.auth.models import User


# from django.forms import ModelForm
# from django import forms


# Create your models here.
# pub_date = models.DateTimeField('date published')


class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WeekOf(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Asset(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Building, related_name='Asset')
    room = models.CharField(max_length=100)
    pub_date = models.DateTimeField('%Y-%m-%d %H:%M', auto_now=True)
    week_of = models.ForeignKey(WeekOf, related_name='Asset')
    image = models.ImageField(upload_to='asset_images', default='default.png', blank=True)
    optional_field = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name + " " + self.location.name

# class AssetForm(ModelForm):
#    class Meta:
#        model = Asset
#        fields = ['asset_name', 'asset_location','asset_room']
