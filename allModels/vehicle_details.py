from django.db  import models
from .  models import BaseModel

class VehicleDetail(BaseModel):
    barcode_number=models.CharField(max_length=60,null=True,blank=True,editable=True)
    vehicle_number=models.CharField(max_length=60,null=True,blank=True,editable=True)
    chessis_number=models.CharField(max_length=60,null=True,blank=True,editable=True)
    vehicle_model=models.CharField(max_length=60,null=True,blank=True,editable=True)
    variants=models.CharField(max_length=60,null=True,blank=True,editable=True)
    color=models.CharField(max_length=60,null=True,blank=True,editable=True)
    date=models.CharField(max_length=50,null=True,blank=True,editable=True)
    status=models.BooleanField(default=True,null=True,blank=True,editable=True)

    def __str__(self):
        return self.barcode_number
