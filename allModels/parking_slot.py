from django.db import models
from .models import BaseModel


class Parking_slot(BaseModel):
    slot_name=models.CharField(max_length=10,null=True,blank=True,editable=True)
    slot_status=models.BooleanField(default=True)


    def __str__(self):
        return self.slot_name