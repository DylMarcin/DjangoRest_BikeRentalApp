from django.contrib import admin
from .models import Client, Bike, Rental

# Register your models here.

admin.site.register(Client)
admin.site.register(Bike)
admin.site.register(Rental)