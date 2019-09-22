from django.db import models
from django.contrib.auth.models import User

class Building(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class WeekOf(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Asset(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    name = models.CharField(max_length=100)
    location = models.ForeignKey(Building, related_name='Asset',on_delete=models.CASCADE,)
    room = models.CharField(max_length=100)
    pub_date = models.DateTimeField('%Y-%m-%d %H:%M', auto_now=True)
    week_of = models.ForeignKey(WeekOf, related_name='Asset',on_delete=models.CASCADE,)
    image = models.ImageField(upload_to='asset_images', default='default.png', blank=True)
    optional_field = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name + " " + self.location.name
