from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib import messages
from allModels import category, add_vehicle, parking_slot,parking_in
from django.shortcuts import get_object_or_404


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
            # slot_status = forms.cleaned_data.get('slot_status')
            self.parking_model.objects.create(slot_name=slot_name, slot_status=True)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='parkingSlot')


class BookVehicle(View):
    vehicle_forms = UserVehicleForm
    vehicle_model = add_vehicle.UserVehicle
    parking_model = parking_slot.Parking_slot
    bookVehicle_add_templates = 'dashboard/add_vehicle.html'
    bookVehicle_view_mplates = 'dashboard/view_vehicle.html'

    def get(self, request, *args, **kwargs):
        if 'bookVehicle' in kwargs:
            available_slot = parking_slot.Parking_slot.objects.filter(slot_status=True)
            return render(request, self.bookVehicle_add_templates, {'form': self.vehicle_forms(), 'available_slot':available_slot})


        elif 'viewVehicle' in kwargs:
            model = self.vehicle_model.objects.all()
            return render(request, self.bookVehicle_view_mplates, {'form': model})

    def post(self, request, *args, **kwargs):
        forms = self.vehicle_forms(request.POST)

        parkingID = request.POST['slot']
        selected_slot = self.parking_model.objects.get(pk=parkingID)
        if forms.is_valid():
            categoty_name = forms.cleaned_data.get('categoty_name')
            Barcode_no = forms.cleaned_data.get('Barcode_no')
            owner_name = forms.cleaned_data.get('owner_name')
            owner_contact = forms.cleaned_data.get('owner_contact')
            vehicle_model = forms.cleaned_data.get('vehicle_model')
            vehicle_no = forms.cleaned_data.get('vehicle_no')
            chessis_no = forms.cleaned_data.get('chessis_no')
            # parking_slot = forms.cleaned_data.get('parking_slot')
            self.vehicle_model.objects.create(categoty_name=categoty_name, Barcode_no=Barcode_no,owner_name=owner_name,
                                              owner_contact=owner_contact,
                                              vehicle_model=vehicle_model, vehicle_no=vehicle_no, chessis_no=chessis_no,
                                              parking_slot=selected_slot)
            # messages.success(request, 'successfully add to database ')
            self.parking_model.objects.filter(pk=parkingID).update(
                slot_status=False
            )
            return redirect(to='bookVehicle')

class ParkingEntry(View):
    parking_entry_forms =ParkingEntryForm
    parking_entry_model = parking_in.ParkingIn
    parking_entry_add_templates = 'dashboard/parking_entry.html'
    vehicle_model = add_vehicle.UserVehicle

    def get(self, request, *args, **kwargs):
        if 'parkingEntry' in kwargs:
            available_barcode = add_vehicle.UserVehicle.objects.all()
            return render(request, self.parking_entry_add_templates, {'form': self.parking_entry_add_templates,'barcode':available_barcode})

    def post(self,request,*args,**kwargs):
        forms=self.parking_entry_forms(request.POST)
        barcode=request.POST['barcode']
        print(barcode)
        entrydate=request.POST['entrydate']
        entrytime=request.POST['entrytime']
        barcode_no = self.vehicle_model.objects.get(pk=barcode)
        print(barcode_no)
        # barcode_no = self.parking_entry_model.objects.get(pk=barcode)
        # print(barcode_no)
        # barcode_no = get_object_or_404(self.parking_entry_model, pk=barcode)

        # barcode_no = add_vehicle.UserVehicle.objects.values('Barcode_no','id')
        # print(barcode_no)
        # return render(request,self.parking_entry_add_templates,{'error': 'Barcode has already taken'})

              # return render(request, self.parking_entry_add_templates, {'error': 'Barcode has already entered'})
        if forms.is_valid():

           self.parking_entry_model.objects.create(
                    user_details=barcode_no, entry_date=entrydate, entry_time=entrytime)

           return redirect(to='parkingEntry')

