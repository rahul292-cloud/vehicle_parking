from django.db import models
from .add_vehicle import UserVehicle
from .models import BaseModel

class ParkingOut(BaseModel):
    user_details=models.ForeignKey(UserVehicle,on_delete=models.CASCADE,null=True,blank=True)
    exit_date = models.DateField(null=False, blank=False)
    exit_time = models.TimeField(null=False, blank=False)

    # def __str__(self):
    #     return self.user_details