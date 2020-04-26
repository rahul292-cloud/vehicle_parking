from django.db import models
from .category import Category
from .models import BaseModel
from .vehicle_details import VehicleDetail
from .parking_slot import Parking_slot


class BookVehicle(BaseModel):
    barcode=models.ForeignKey(VehicleDetail,on_delete=models.CASCADE,null=False,blank=False)
    vehicle_no=models.CharField(max_length=100,null=False,blank=False,editable=True)
    chessis_no=models.CharField(max_length=100,null=False,blank=False,editable=True)
    vehicle_model=models.CharField(max_length=100,null=False,blank=False,editable=True)
    variants=models.CharField(max_length=100,null=False,blank=False,editable=True)
    color=models.CharField(max_length=100,null=False,blank=False,editable=True)
    parking_slot=models.ForeignKey(Parking_slot,on_delete=models.CASCADE,null=True,blank=True)
    booking_date = models.DateTimeField(null=False, blank=False)
    booking_exit_date=models.DateTimeField(null=False,blank=False)


    status=models.BooleanField(default=True,null=True,blank=True,editable=True)

    def __str__(self):
        return str(self.barcode)