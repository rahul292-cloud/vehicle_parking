from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib import messages
from allModels import category, add_vehicle, parking_slot,parking_in


# Create your views here.
def index(request):
    return render(request, 'dashboard/base.html')


class Category(View):
    category_forms = CategoryForm
    category_model = category.Category
    category_add_templates = 'dashboard/categoryAdd.html'

    def get(self, request, *args, **kwargs):
        if 'category' in kwargs:
            return render(request, self.category_add_templates, {'form': self.category_forms()})

    def post(self, request, *args, **kwargs):
        forms = self.category_forms(request.POST)
        if forms.is_valid():
            category_name = forms.cleaned_data.get('category_name')
            self.category_model.objects.create(category_name=category_name)
            # messages.success(request,'successfully add to database ')
            return redirect(to='category')


class ParkingSlot(View):
    parking_forms = ParkingSlotForm
    parking_model = parking_slot.Parking_slot
    parking_add_templates = 'dashboard/parking_slot_add.html'

    def get(self, request, *args, **kwargs):
        if 'parkingSlot' in kwargs:
            return render(request, self.parking_add_templates, {'form': self.parking_forms()})

    def post(self, request, *args, **kwargs):
        forms = self.parking_forms(request.POST)
        if forms.is_valid():
            slot_name = forms.cleaned_data.get('slot_name')
            slot_status = forms.cleaned_data.get('slot_status')
            self.parking_model.objects.create(slot_name=slot_name, slot_status=slot_status)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='parkingSlot')


class BookVehicle(View):
    vehicle_forms = UserVehicleForm
    vehicle_model = add_vehicle.UserVehicle
    bookVehicle_add_templates = 'dashboard/add_vehicle.html'

    def get(self, request, *args, **kwargs):
        if 'bookVehicle' in kwargs:
            return render(request, self.bookVehicle_add_templates, {'form': self.vehicle_forms()})

    def post(self, request, *args, **kwargs):
        forms = self.vehicle_forms(request.POST)
        if forms.is_valid():
            categoty_name = forms.cleaned_data.get('categoty_name')
            owner_name = forms.cleaned_data.get('owner_name')
            owner_contact = forms.cleaned_data.get('owner_contact')
            vehicle_model = forms.cleaned_data.get('vehicle_model')
            vehicle_no = forms.cleaned_data.get('vehicle_no')
            chessis_no = forms.cleaned_data.get('chessis_no')
            parking_slot = forms.cleaned_data.get('parking_slot')
            self.vehicle_model.objects.create(categoty_name=categoty_name, owner_name=owner_name,
                                              owner_contact=owner_contact,
                                              vehicle_model=vehicle_model, vehicle_no=vehicle_no, chessis_no=chessis_no,
                                              parking_slot=parking_slot)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='bookVehicle')

class ParkingEntry(View):
    parking_entry_forms =ParkingEntryForm
    parking_entry_model = parking_in.ParkingIn
    parking_entry_add_templates = 'dashboard/parking_entry.html'

    def get(self, request, *args, **kwargs):
        if 'parkingEntry' in kwargs:
            return render(request, self.parking_entry_add_templates, {'form': self.parking_entry_forms()})