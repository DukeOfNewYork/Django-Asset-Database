from django.contrib import admin
from .models import Asset, Building, WeekOf
# Register your models here.

admin.site.register(Asset)
admin.site.register(Building)
admin.site.register(WeekOf)
