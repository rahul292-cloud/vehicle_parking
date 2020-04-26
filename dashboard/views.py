from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from allModels import category, add_vehicle, parking_slot,parking_in,parkingOut,vehicle_details,booking
from django.shortcuts import get_object_or_404
import openpyxl
import xlrd

# Create your views here.
def register(request):
    return render(request, 'dashboard/register.html')

# class Vehicle_Excel(View):
#     vehicle_details_form=VehicleDetailsForm
#     vehicle_details_model=vehicle_details.VehicleDetails
#     vehicle_details_templates="dashboard/vehicleDetails.html"
#
#     def get(self, request, *args, **kwargs):
#         if 'vehicle_excel' in kwargs:
#             return render(request, self.vehicle_details_templates, {'form': self.vehicle_details_form})


    # def get(self, request, *args, **kwargs):
    #     if 'vehicle_excel' in kwargs:
    #         return render(request, self.vehicle_details_templates, {'form': self.vehicle_details_form()})

class Vehicle(View):
    vehicle_details_form = VehicleDetailsForm
    vehicle_details_templates = "dashboard/vehicleDetails.html"
    # vehicle_details_templates = "dashboard/vehicle_view.html"
    model=vehicle_details.VehicleDetail
    def get(self,request,*args,**kwargs):
        if 'vehicle' in kwargs:
          allvehicle=self.model.objects.all()
          return render(request,self.vehicle_details_templates, {'form':self.vehicle_details_form(),'model':allvehicle})

    def post(self, request, *args, **kwargs):
        form = self.vehicle_details_form(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            print(input_excel)
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            print(sheet)
            # data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
            barcode_number= []
            vehicle_number= []
            chessis_number= []
            vehicle_model= []
            variants= []
            color= []
            # date= []
            print(barcode_number)

            for i in range(sheet.nrows):
                barcode_number.append(sheet.cell_value(i, 0))
                vehicle_number.append(sheet.cell_value(i, 1))
                chessis_number.append(sheet.cell_value(i, 2))
                vehicle_model.append(sheet.cell_value(i, 3))
                variants.append(sheet.cell_value(i, 4))
                color.append(sheet.cell_value(i, 5))
                # date.append(sheet.cell_value(i, 6))

            barcode_number.pop(0)
            vehicle_number.pop(0)
            chessis_number.pop(0)
            vehicle_model.pop(0)
            variants.pop(0)
            color.pop(0)
            # date.pop(0)


            for i in range(len(barcode_number)):
                self.model.objects.get_or_create(barcode_number=barcode_number[i], vehicle_number=vehicle_number[i],
                                                 chessis_number=chessis_number[i], vehicle_model=vehicle_model[i], variants=variants[i],
                                                 color=color[i],status=True
                                                 )
            return redirect(to='vehicle')


#     else:
#         excel_file = request.FILES["excel_file"]
#
#         # you may put validations here to check extension or file size
#
#         wb = openpyxl.load_workbook(excel_file)
#
#         # getting all sheets
#         sheets = wb.sheetnames
#         print(sheets)
#
#         # getting a particular sheet
#         worksheet = wb["Sheet1"]
#         print(worksheet)
#
#         # getting active sheet
#         active_sheet = wb.active
#         print(active_sheet)
#
#         # reading a cell
#         print(worksheet["A1"].value)
#
#         excel_data = list()
#         # iterating over the rows and
#         # getting value from each cell in row
#         for row in worksheet.iter_rows():
#             row_data = list()
#             for cell in row:
#                 row_data.append(str(cell.value))
#                 print(cell.value)
#             excel_data.append(row_data)
#
#         return render(request, 'dashboard/vehicleDetails.html', {"excel_data": excel_data})


def index(request):
    return render(request, 'dashboard/base.html')

class LoginPage(View):
    login_template = "dashboard/login.html"

    def get(self, request, *args, **kwargs):

        if 'login' in kwargs:
            context = {}
            return render(request, self.login_template, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect(to='dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, self.login_template)





class Dashboard(View):
    def get(self,request,*args,**kwargs):
        if 'dashboard' in kwargs:
            slot = parking_slot.Parking_slot.objects.all()
            totalslots = slot.count()

            avaiableslots = parking_slot.Parking_slot.objects.filter(slot_status=True)
            avaiable = avaiableslots.count()

            bookings = add_vehicle.UserVehicle.objects.all()
            booking = bookings.count()
            context = {
                'totalslot': totalslots, 'avaiable': avaiable, 'user': booking
            }
            return render(request, 'dashboard/Dashboard.html', context)


class CategoryAdd(View):
    category_forms = CategoryForm
    category_model = category.Category
    category_add_templates = 'dashboard/categoryAdd.html'
    category_view_templates = 'dashboard/categoryView.html'

    def get(self, request, *args, **kwargs):
        if 'category' in kwargs:
            return render(request, self.category_add_templates, {'form': self.category_forms()})
        # elif 'categoryView' in kwargs:
        #     model=self.category_model.objects.all()
        #     return render(request,self.category_view_templates, {'form': model})
        elif 'categoryView' in kwargs:
            model = self.category_model.objects.all()
            print(model)
            return render(request, self.category_view_templates, {'category': model})

    def post(self, request, *args, **kwargs):
        forms = self.category_forms(request.POST)
        if forms.is_valid():
            category_name = forms.cleaned_data.get('category_name')
            self.category_model.objects.create(
                category_name=category_name
            )
            # messages.success(request,'successfully add to database ')
            return redirect(to='category')
        # if forms.is_valid():
        #     category_name = forms.cleaned_data.get('category_name')
        #     self.category_model.objects.create(category_name=category_name)
        #     # messages.success(request,'successfully add to database ')
        #     return redirect(to='categoryView')



class CategoryEdit(View):
    category_forms = CategoryForm
    category_model = category.Category
    category_edit_templates = 'dashboard/categoryEdit.html'

    def get(self, request, *args, **kwargs):
        if 'categoryEdit' in kwargs:
            editmodel = self.category_model.objects.get(id=kwargs.get('object_id'))
            editform  = self.category_forms(instance=editmodel)
            return render(request, self.category_edit_templates, {'categoryUpdate': editform})

    def post(self, request, *args, **kwargs):
        forms = self.category_forms(request.POST)
        if forms.is_valid():
            category_name = forms.cleaned_data.get('category_name')
            self.category_model.objects.filter(id=kwargs.get('object_id')).update(
                category_name=category_name
            )
            # messages.success(request,'successfully add to database ')
            return redirect(to='categoryView')


class ParkingSlot(View):
    parking_forms = ParkingSlotForm
    parking_model = parking_slot.Parking_slot
    parking_add_templates = 'dashboard/parking_slot_add.html'
    parking_view_templates = 'dashboard/parking_slot_view.html'

    def get(self, request, *args, **kwargs):
        if 'parkingSlot' in kwargs:
            return render(request, self.parking_add_templates, {'form': self.parking_forms()})
        elif 'parkingSlotView' in kwargs:
            model=self.parking_model.objects.all()
            return render(request,self.parking_view_templates,{'parking':model})

    def post(self, request, *args, **kwargs):
        forms = self.parking_forms(request.POST)
        if forms.is_valid():
            slot_name = forms.cleaned_data.get('slot_name')
            # slot_status = forms.cleaned_data.get('slot_status')
            self.parking_model.objects.create(slot_name=slot_name, slot_status=True)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='parkingSlot')

class ParkingSlotEdit(View):
    parking_forms = ParkingSlotForm
    parking_model = parking_slot.Parking_slot
    parking_edit_templates = 'dashboard/parking_slot_edit.html'

    def get(self, request, *args, **kwargs):
        if 'parkingSlotEdit' in kwargs:
            editmodel=self.parking_model.objects.get(id=kwargs.get('object_id'))
            editForm=self.parking_forms(instance=editmodel)
            return render(request,self.parking_edit_templates,{'Updateparking':editForm})

    def post(self, request, *args, **kwargs):
        forms = self.parking_forms(request.POST)
        if forms.is_valid():
            slot_name = forms.cleaned_data.get('slot_name')
            # slot_status = forms.cleaned_data.get('slot_status')
            self.parking_model.objects.filter(id=kwargs.get('object_id')).update(slot_name=slot_name)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='parkingSlotView')

#------------------new



class Booking(View):
    booking_forms = BookVehicleForm
    booking_model = booking.BookVehicle
    parking_model = parking_slot.Parking_slot
    booking_add_templates = 'dashboard/bookingAdd.html'
    booking_view_mplates = 'dashboard/bookingView.html'

    def get(self, request, *args, **kwargs):
        if 'booking' in kwargs:
            available_slot = parking_slot.Parking_slot.objects.filter(slot_status=True)
            barcode_slot = vehicle_details.VehicleDetail.objects.all()
            # barcode=
            return render(request, self.booking_add_templates, {'form': self.booking_forms(), 'available_slot':available_slot,'barcode_slots':barcode_slot})


        elif 'bookingView' in kwargs:
            model = self.booking_model.objects.all()
            return render(request, self.booking_view_mplates, {'form': model})

    def post(self, request, *args, **kwargs):
        forms = self.booking_forms(request.POST)



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
            self.booking_model.objects.create(categoty_name=categoty_name, Barcode_no=Barcode_no,owner_name=owner_name,
                                              owner_contact=owner_contact,
                                              vehicle_model=vehicle_model, vehicle_no=vehicle_no, chessis_no=chessis_no,
                                              parking_slot=selected_slot)
            # messages.success(request, 'successfully add to database ')
            self.parking_model.objects.filter(pk=parkingID).update(
                slot_status=False
            )

            return redirect(to='bookVehicle')




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

class EditVehicle(View):
    vehicle_forms = UserVehicleForm
    vehicle_model = add_vehicle.UserVehicle
    parking_model = parking_slot.Parking_slot
    bookVehicle_edit_mplates = 'dashboard/edit_vehicle.html'

    def get(self, request, *args, **kwargs):
        if 'EditVehicle' in kwargs:
            available_slot = parking_slot.Parking_slot.objects.filter(slot_status=True)
            editmodel = self.vehicle_model.objects.get(id=kwargs.get('object_id'))
            editForm=self.vehicle_forms(instance=editmodel)
            return render(request, self.bookVehicle_edit_mplates, {'UpdateVehicle': editForm,'available_slot':available_slot})

    def post(self, request, *args, **kwargs):
        forms = self.vehicle_forms(request.POST)

        # parkingID = request.POST['slot']
        # selected_slot = self.parking_model.objects.get(pk=parkingID)
        if forms.is_valid():
            categoty_name = forms.cleaned_data.get('categoty_name')
            Barcode_no = forms.cleaned_data.get('Barcode_no')
            owner_name = forms.cleaned_data.get('owner_name')
            owner_contact = forms.cleaned_data.get('owner_contact')
            vehicle_model = forms.cleaned_data.get('vehicle_model')
            vehicle_no = forms.cleaned_data.get('vehicle_no')
            chessis_no = forms.cleaned_data.get('chessis_no')
            parking_slot = forms.cleaned_data.get('parking_slot')
            self.vehicle_model.objects.filter(id=kwargs.get('object_id')).update(categoty_name=categoty_name, Barcode_no=Barcode_no,owner_name=owner_name,
                                              owner_contact=owner_contact,
                                              vehicle_model=vehicle_model, vehicle_no=vehicle_no, chessis_no=chessis_no,
                                              parking_slot=parking_slot)
            # messages.success(request, 'successfully add to database ')
            # self.parking_model.objects.filter(pk=parkingID).update(
            #     slot_status=False
            # )
            return redirect(to='viewVehicle')

# ----------------------------end old
class ParkingEntry(View):
    parking_entry_forms =ParkingEntryForm
    parking_entry_model = parking_in.ParkingIn
    parking_entry_add_templates = 'dashboard/parking_entry.html'
    vehicle_model = add_vehicle.UserVehicle

    parking_entry_view_templates = 'dashboard/parkingEntry_view.html'

    def get(self, request, *args, **kwargs):
        if 'parkingEntry' in kwargs:
            available_barcode = add_vehicle.UserVehicle.objects.filter(status=True)
            return render(request, self.parking_entry_add_templates, {'form': self.parking_entry_forms(),'barcode':available_barcode})
        elif 'parkingEntryView' in kwargs:
            model=self.parking_entry_model.objects.all()
            return render(request,self.parking_entry_view_templates,{'parkingView':model})

    # def get(self, request, *args, **kwargs):
    #     if 'parkingEntry' in kwargs:
    #         available_barcode = add_vehicle.UserVehicle.objects.all()
    #         return render(request, self.parking_entry_add_templates, {'form': self.parking_entry_add_templates,'barcode':available_barcode})

    def post(self,request,*args,**kwargs):
        barcode=request.POST['barcode']
        print(barcode)
        entrydate=request.POST['entrydate']
        entrytime=request.POST['entrytime']
        barcode_no = add_vehicle.UserVehicle.objects.get(pk=barcode)

        entrysave = parking_in.ParkingIn.objects.create(
                    user_details=barcode_no, entry_date=entrydate, entry_time=entrytime)
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

        add_vehicle.UserVehicle.objects.filter(id=barcode).update(
            status=False
        )
        return redirect(to='parkingEntry')


class ParkingEntryEdit(View):
    parking_entry_forms =ParkingEntryForm
    parking_entry_model = parking_in.ParkingIn
    parking_entry_edit_templates = 'dashboard/parkingEntry_edit.html'

    def get(self, request, *args, **kwargs):
        if 'parkingEntryEdit' in kwargs:
            editmodel=self.parking_entry_model.objects.get(id=kwargs.get('object_id'))
            editForm=self.parking_entry_forms(instance=editmodel)
            return render(request,self.parking_entry_edit_templates,{'UpdateparkingEntry':editForm})

    def post(self,request,*args,**kwargs):
         forms=self.parking_entry_forms(request.POST)
         if forms.is_valid():
             user_details = forms.cleaned_data.get('user_details')
             entry_date = forms.cleaned_data.get('entry_date')
             entry_time = forms.cleaned_data.get('entry_time')
             self.parking_entry_model.objects.filter(id=kwargs.get('object_id')).update(
                    user_details=user_details, entry_date=entry_date, entry_time=entry_time)
             return redirect(to='parkingEntryView')

class ParkingExit(View):
    parking_exit_forms =ParkingOutForm
    parking_exit_model = parkingOut.ParkingOut
    parking_exit_add_templates = 'dashboard/parkingOutAdd.html'
    parking_exit_view_templates = 'dashboard/parkingExit_view.html'

    def get(self, request, *args, **kwargs):
        if 'parkingExit' in kwargs:
            available_barcode = add_vehicle.UserVehicle.objects.filter(status=False)
            return render(request, self.parking_exit_add_templates, {'form': self.parking_exit_forms(),'barcode':available_barcode})
        elif 'parkingExitView' in kwargs:
            model=self.parking_exit_model.objects.all()
            return render(request,self.parking_exit_view_templates,{'parkingExitView':model})

    def post(self,request,*args,**kwargs):
        barcode=request.POST['barcode']
        exitdate=request.POST['exitdate']
        exittime=request.POST['exittime']
        barcode_no = add_vehicle.UserVehicle.objects.get(pk=barcode)

        exitsave=parkingOut.ParkingOut.objects.create(
                    user_details=barcode_no, exit_date=exitdate, exit_time=exittime)

        # add_vehicle.UserVehicle.objects.filter(id=barcode).update(
        #     status=True
        # )
        return redirect(to='parkingExit')
