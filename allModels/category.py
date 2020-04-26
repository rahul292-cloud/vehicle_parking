from django.db import models
from .models import BaseModel


class Category(BaseModel):
    category_name=models.CharField(max_length=100,null=False,blank=False,editable=True)
    status=models.BooleanField(default=True,null=False,blank=False,editable=True)

    def __str__(self):
        return self.category_name
