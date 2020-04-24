from django.contrib import admin
from .category import Category
from .add_vehicle import UserVehicle
from .parking_slot import Parking_slot
from .parking_in import ParkingIn
from .parkingOut import ParkingOut
# Register your models here.

admin.site.register(Category)
admin.site.register(UserVehicle)
admin.site.register(Parking_slot)
admin.site.register(ParkingIn)
admin.site.register(ParkingOut)