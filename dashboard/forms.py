import os
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from allModels import category,add_vehicle,parking_slot,parking_in
    # ,,parking_out,
# from django.forms import ModelForm

class DateInput(forms.DateInput):
    input_type='date'


class CategoryForm(forms.ModelForm):
    class Meta:
        model=category.Category
        fields=[
            'category_name'
        ]

        widgets={
            'category_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),

        }
#
class ParkingSlotForm(forms.ModelForm):

    class Meta:
        model=parking_slot.Parking_slot
        fields=[
            'slot_name','slot_status'
        ]
        widgets={
            'slot_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

#
class ParkingEntryForm(forms.ModelForm):
    class Meta:
        model=parking_in.ParkingIn
        fields=[
            'user_details','entry_date','entry_time'
        ]
        # forms.DateInput(format='%d/%m/%Y')

        widgets={
            'user_details': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'entry_date':  forms.DateInput(format='%d/%m/%Y'),
            # 'entry_time': forms.TimeField(format='%H:%M'),
        }

#
#
# class ParkingOutForm(forms.ModelForm):
#     class Meta:
#         model=parking_out.ParkingOut
#         fields=[
#             'user_details','parking_slot','exit_time'
#         ]
#
#         wedgets={
#             'user_details': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
#             'parking_slot': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
#             'entry_date': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
#             'entry_time': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
#
#         }
#
#
class UserVehicleForm(forms.ModelForm):
    class Meta:
        model=add_vehicle.UserVehicle
        fields=[
            'categoty_name','Barcode_no','owner_name','owner_contact','vehicle_model','vehicle_no','chessis_no','parking_slot',
            ]
        widgets={
            'categoty_name': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'Barcode_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'owner_name': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'owner_contact': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'vehicle_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'chessis_no': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'parking_slot': forms.Select(attrs={'class': 'form-control form-control-sm'}),

        }


