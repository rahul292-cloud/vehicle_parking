from django.db import models
from .category import Category
from .models import BaseModel
from .parking_slot import Parking_slot


class UserVehicle(BaseModel):
    categoty_name=models.ForeignKey(Category,on_delete=models.CASCADE,null=False,blank=False)
    Barcode_no=models.CharField(max_length=100,null=True,blank=True)
    owner_name=models.CharField(max_length=100,null=True,blank=True)
    owner_contact=models.CharField(max_length=100,null=True,blank=True)
    vehicle_model=models.CharField(max_length=100,null=False,blank=False,editable=True)
    vehicle_no=models.CharField(max_length=100,null=False,blank=False,editable=True)
    chessis_no=models.CharField(max_length=100,null=False,blank=False,editable=True)
    parking_slot=models.ForeignKey(Parking_slot,on_delete=models.CASCADE,null=True,blank=True)
    status=models.BooleanField(default=True,null=True,blank=True,editable=True)

    def __str__(self):
        return self.Barcode_no