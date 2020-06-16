from django.db import models
from .category import Category
from .models import BaseModel
from .vehicle_details import VehicleDetail
from .parking_slot import Parking_slot
from django.utils import timezone


class BookVehicle(BaseModel):
    barcode_details=models.ForeignKey(VehicleDetail,on_delete=models.CASCADE,null=False,blank=False)
    vehicle_no=models.CharField(max_length=100,null=False,blank=False,editable=True)
    chessis_no=models.CharField(max_length=100,null=False,blank=False,editable=True)
    vehicle_model=models.CharField(max_length=100,null=False,blank=False,editable=True)
    variants=models.CharField(max_length=100,null=True,blank=True,editable=True)
    color=models.CharField(max_length=100,null=False,blank=False,editable=True)
    parking_slot=models.ForeignKey(Parking_slot,on_delete=models.CASCADE,null=True,blank=True)
    booking_date = models.DateTimeField(default=timezone.now,null=True, blank=True)
    booking_exit_date=models.DateTimeField(null=True,blank=True)
    status=models.BooleanField(default=True,null=True,blank=True,editable=True)

    def __str__(self):
        return str(self.barcode_details)




class ParkingExit(BaseModel):
    barcode = models.ForeignKey(BookVehicle, on_delete=models.CASCADE, null=False, blank=False)
    vehicle_no = models.CharField(max_length=100, null=False, blank=False, editable=True)
    chessis_no = models.CharField(max_length=100, null=False, blank=False, editable=True)
    vehicle_model = models.CharField(max_length=100, null=False, blank=False, editable=True)
    variants = models.CharField(max_length=100, null=True, blank=True, editable=True)
    color = models.CharField(max_length=100, null=False, blank=False, editable=True)
    slot = models.CharField(max_length=100,default="", null=False, blank=False, editable=True)
    # parking_slot = models.ForeignKey(Parking_slot, on_delete=models.CASCADE, null=True, blank=True)
    exit_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    status = models.BooleanField(default=True, null=True, blank=True, editable=True)

    def __str__(self):
        return str(self.barcode)






class AmcInventory(models.Model):
    customer_name =models.CharField(max_length=100,null=False,blank=False,editable=True)
    location =models.CharField(max_length=100,null=False,blank=False,editable=True)
    installation_location =models.CharField(max_length=100,null=False,blank=False,editable=True)
    product_description =models.CharField(max_length=100,null=False,blank=False,editable=True)
    device_type =models.CharField(max_length=100,null=True,blank=True,editable=True)
    model_number =models.CharField(max_length=100,null=True,blank=True,editable=True)
    serial_number =models.CharField(max_length=100,null=True,blank=True,editable=True)
    amc_start_date =models.DateField(null=True,blank=True)
    amc_end_date =models.DateField(null=True,blank=True)
    warranty_start_date =models.DateField(null=True,blank=True)
    warranty_end_date =models.DateField(null=True,blank=True)


    def __str__(self):
        return self.customer_name


class AmcInventoryHistory(models.Model):
    # amc_inventory=models.ForeignKey(AmcInventory,on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, null=False, blank=False, editable=True)
    location = models.CharField(max_length=100, null=False, blank=False, editable=True)
    installation_location = models.CharField(max_length=100, null=False, blank=False, editable=True)
    product_description = models.CharField(max_length=100, null=False, blank=False, editable=True)
    device_type = models.CharField(max_length=100, null=True, blank=True, editable=True)
    model_number = models.CharField(max_length=100, null=True, blank=True, editable=True)
    serial_number = models.CharField(max_length=100, null=True, blank=True, editable=True)
    amc_start_date = models.DateField(null=True, blank=True)
    amc_end_date = models.DateField(null=True, blank=True)
    warranty_start_date = models.DateField(null=True, blank=True)
    warranty_end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.amc_inventory

