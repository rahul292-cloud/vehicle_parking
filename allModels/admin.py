from django.contrib import admin
from .category import Category
from .add_vehicle import UserVehicle

# Register your models here.
admin.site.register(Category)
admin.site.register(UserVehicle)