from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# from .decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from allModels import category, add_vehicle, parking_slot, parking_in, parkingOut, vehicle_details, booking, \
    vehicle_details
from allModels.booking import ParkingExit
from django.db.models import Value as V

from django.shortcuts import get_object_or_404
import openpyxl
import xlrd
from django.db.models.functions import Cast, Concat, Coalesce
from django.db.models import (Case, CharField, Count, DateTimeField,
                              ExpressionWrapper, F, FloatField, Func, Max, Min,
                              Prefetch, Q, Sum, Value, When, Subquery)


# Create your views here.


def index(request):
    return render(request, 'dashboard/base.html')

def Location(request):
    return render(request, 'dashboard/location.html')


class RegisterPage(View):
    register_template = "dashboard/register.html"

    # @method_decorator(unauthenticated_user)
    def get(self, request, *args, **kwargs):
        if 'register' in kwargs:
            # form = CreateUserForm()
            # context = {'form': form}
            return render(request, self.register_template)

    def post(self, request, *args, **kwargs):
        if request.POST['password1'] == request.POST['password2']:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            try:
                user = User.objects.get(username=username)
                return render(request, self.register_template, {'error': 'Username has already existed'})
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password1, email=email)
                login(request, user)
                messages.success(request, 'Account was created for ' + username)
                return redirect(to='login')
        else:
            return render(request, self.register_template, {'error': 'Password does not match'})

        # form = CreateUserForm(request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     username = form.cleaned_data.get('username')

        # group = Group.objects.get(name='customer')
        # user.groups.add(group)
        # emp = employee.Employee.objects.create(
        #     user=user
        # )


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
            request.session.set_expiry(86400)  # sets the exp. value of the session
            login(request, user)

            return redirect(to='dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect')
            return render(request, self.login_template)


class Chart(View):
    def get(self, request, *args, **kwargs):
        if 'chartView' in kwargs:
            slot = parking_slot.Parking_slot.objects.all()
            totalslots = slot.count()

            booking_model = booking.BookVehicle.objects.all()
            booking_vehicle = booking.BookVehicle.objects.filter(status=True)
            unbooking_vehicle = booking.BookVehicle.objects.filter(status=False)
            all_book = booking_model.count()
            booking_book = booking_vehicle.count()
            unbooking_book = unbooking_vehicle.count()

            exit_model = booking.ParkingExit.objects.all()
            all_exit = exit_model.count()

            avaiableslots = parking_slot.Parking_slot.objects.filter(slot_status=True)
            avaiable = avaiableslots.count()

            totalvehicle = vehicle_details.VehicleDetail.objects.all()
            countVehicle = totalvehicle.count()

            labels: ['Total Slot ', 'Available SLot', 'Total Vehicle Details', 'Total Exit Vehicle',
                     'Total Booking Vehicle']

            data = {
                # 'label': labels,
                'totalslot': totalslots, 'avaiable': avaiable, 'user': countVehicle, 'book': all_book, 'exit': all_exit,
                'booking_vehicle': booking_book
            }
            return JsonResponse(data, safe=False)

class Dashboard(View):
    def get(self, request, *args, **kwargs):
        # @method_decorator(login_required(login_url='login'))
        # @method_decorator(allowed_users(allowed_roles=['admin']))
        if 'dashboard' in kwargs:
            slot = parking_slot.Parking_slot.objects.all()
            totalslots = slot.count()

            booking_model = booking.BookVehicle.objects.all()
            booking_vehicle = booking.BookVehicle.objects.filter(status=True)
            unbooking_vehicle = booking.BookVehicle.objects.filter(status=False)
            all_book = booking_model.count()
            booking_book = booking_vehicle.count()
            unbooking_book = unbooking_vehicle.count()

            exit_model = booking.ParkingExit.objects.all()
            all_exit = exit_model.count()

            avaiableslots = parking_slot.Parking_slot.objects.filter(slot_status=False)
            avaiable = avaiableslots.count()

            totalvehicle = vehicle_details.VehicleDetail.objects.all()
            countVehicle = totalvehicle.count()

            context = {
                'totalslot': totalslots, 'bookingSlot': avaiable, 'user': countVehicle, 'book': all_book, 'exit': all_exit,
                'booking_vehicle': booking_book, 'unbooking': unbooking_book
            }
            return render(request, 'dashboard/Dashboard.html', context)


class Vehicle(View):
    vehicle_details_form = VehicleDetailsForm
    vehicle_details_templates = "dashboard/vehicleDetails.html"
    # vehicle_details_templates = "dashboard/vehicle_view.html"
    model = vehicle_details.VehicleDetail

    def get(self, request, *args, **kwargs):
        if 'vehicle' in kwargs:
            allvehicle = self.model.objects.all().order_by('-id')
            return render(request, self.vehicle_details_templates,
                          {'form': self.vehicle_details_form(), 'model': allvehicle})

    def post(self, request, *args, **kwargs):
        form = self.vehicle_details_form(request.POST, request.FILES)
        if form.is_valid():
            input_excel = request.FILES['input_excel']
            # print(input_excel)
            book = xlrd.open_workbook(file_contents=input_excel.read())
            sheet = book.sheet_by_index(0)
            # print(sheet)
            # data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
            barcode_number = []
            vehicle_number = []
            chessis_number = []
            vehicle_model = []
            variants = []
            color = []
            # date= []
            # print(barcode_number)

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
                                                 chessis_number=chessis_number[i], vehicle_model=vehicle_model[i],
                                                 variants=variants[i],
                                                 color=color[i], status=True
                                                 )
            return redirect(to='vehicle')


class ParkingSlot(View):
    parking_forms = ParkingSlotForm
    parking_model = parking_slot.Parking_slot
    parking_add_templates = 'dashboard/parking_slot_add.html'
    parking_view_templates = 'dashboard/parking_slot_view.html'

    def get(self, request, *args, **kwargs):
        if 'parkingSlot' in kwargs:
            return render(request, self.parking_add_templates, {'form': self.parking_forms()})
        elif 'parkingSlotView' in kwargs:
            model = self.parking_model.objects.all().order_by('-id')
            return render(request, self.parking_view_templates, {'parking': model})

    def post(self, request, *args, **kwargs):
        forms = self.parking_forms(request.POST)
        if forms.is_valid():
            slot_name = forms.cleaned_data.get('slot_name')
            # slot_status = forms.cleaned_data.get('slot_status')
            self.parking_model.objects.create(slot_name=slot_name, slot_status=True)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='parkingSlotView')


class ParkingSlotEdit(View):
    parking_forms = ParkingSlotForm
    parking_model = parking_slot.Parking_slot
    parking_edit_templates = 'dashboard/parking_slot_edit.html'

    def get(self, request, *args, **kwargs):
        if 'parkingSlotEdit' in kwargs:
            editmodel = self.parking_model.objects.get(id=kwargs.get('object_id'))
            editForm = self.parking_forms(instance=editmodel)
            return render(request, self.parking_edit_templates, {'Updateparking': editForm})

    def post(self, request, *args, **kwargs):
        forms = self.parking_forms(request.POST)
        if forms.is_valid():
            slot_name = forms.cleaned_data.get('slot_name')
            # slot_status = forms.cleaned_data.get('slot_status')
            self.parking_model.objects.filter(id=kwargs.get('object_id')).update(slot_name=slot_name)
            # messages.success(request, 'successfully add to database ')
            return redirect(to='parkingSlotView')


class ParkingSlotDelete(View):
    parking_delete_template = 'dashboard/parking_slot_delete.html'
    parking_model = parking_slot.Parking_slot

    # @method_decorator(login_required(login_url='login'))
    # @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request, *args, **kwargs):
        if 'parkingSlotDelete' in kwargs:
            item = self.parking_model.objects.get(id=kwargs.get("object_id"))
            return render(request, self.parking_delete_template, {'item': item})

    def post(self, request, *args, **kwargs):
        item = self.parking_model.objects.get(id=kwargs.get("object_id"))
        item.delete()
        return redirect(to="parkingSlotView")


class Booking(View):
    booking_forms = BookVehicleForm
    booking_model = booking.BookVehicle
    vehicle_model = vehicle_details.VehicleDetail
    parking_model = parking_slot.Parking_slot
    booking_add_templates = 'dashboard/bookingAdd.html'
    booking_view_templates = 'dashboard/bookingView.html'
    booking_print_templates = 'dashboard/bookingPrint.html'

    def get_data(self, request, id=None, *args, **kwargs):
        print(id)
        if 'barcode_details' in kwargs:
            # print(request.POST.get('barcode_details'))

            data = vehicle_details.VehicleDetail.objects.filter(pk=request.POST.get('barcode_details')).values(
                 'vehicle_number', 'chessis_number', 'vehicle_model', 'variants', 'color',
                'status'
            )
            #     .annotate(
            #     client_booking_date=ExpressionWrapper(Func(F('date'), Value("DD/MM/YYYY"), function='TO_CHAR'),
            #                                     output_field=CharField()),
            # )

            return list(data)
        print_data = self.booking_model.objects.filter(id=id).values('vehicle_no', 'chessis_no',
                                                                     'vehicle_model',
                                                                     'variants',
                                                                     'color'

                                                                     ).annotate(
            print_barcode_details=F('barcode_details__barcode_number'),
            print_booking_date=ExpressionWrapper(Func(F('booking_date'), Value("DD/MM/YYYY"), function='TO_CHAR'),
                                                 output_field=CharField()), print_slot=F('parking_slot__slot_name')
        )
        return list(print_data)

    def get(self, request, *args, **kwargs):
        if 'booking' in kwargs:
            available_slot = parking_slot.Parking_slot.objects.filter(slot_status=True)
            available_barcode = self.vehicle_model.objects.filter(status=True)
            return render(request, self.booking_add_templates,
                          {'form': self.booking_forms(), 'available_slot': available_slot,
                           'available_barcode': available_barcode})

        if 'printDetails' in kwargs:
            data = self.get_data(request, id=kwargs.get('object_id'))
            model = self.booking_model.objects.get(id=kwargs.get('object_id'))
            # print(model)
            return render(request, self.booking_print_templates, {'print_data': data, 'printView': model})

        elif 'bookingView' in kwargs:
            model = self.booking_model.objects.all().order_by('-id') \
                .annotate(
                client_booking_time=ExpressionWrapper(Func(F('booking_date'), Value("HH24:MI:SS"), function='TO_CHAR'),
                                                      output_field=CharField()),
                client_booking_date=ExpressionWrapper(Func(F('booking_date'), Value("DD/MM/YYYY"), function='TO_CHAR'),output_field=CharField()),
            )

            return render(request, self.booking_view_templates, {'form': model})

    def post(self, request, *args, **kwargs):
        if 'barcode_details' in kwargs:
            data = self.get_data(request, barcode_details='')
            # print(data)
            return JsonResponse(data, safe=False)

        forms = self.booking_forms(request.POST)
        parkingID = request.POST['slot']
        selected_slot = self.parking_model.objects.get(pk=parkingID)

        barcodeID = request.POST['barcode']
        selected_barcode = self.vehicle_model.objects.get(pk=barcodeID)
        # print(parkingID)
        # print(selected_slot)
        # print(selected_barcode)

        vehicle_no = request.POST['vehicle_no']
        chessis_no = request.POST['chessis_no']
        vehicle_model = request.POST['vehicle_model']
        variants = request.POST['variants']
        color = request.POST['color']
        # parking_slot = request.POST['parking_slot']
        exit_data = self.booking_model.objects.create(barcode_details=selected_barcode, vehicle_no=vehicle_no,
                                                      chessis_no=chessis_no, vehicle_model=vehicle_model
                                                      , variants=variants, color=color, parking_slot=selected_slot)

        update_slot_status = self.parking_model.objects.filter(pk=parkingID).update(
            slot_status=False
        )
        update_vehicle_status = self.vehicle_model.objects.filter(pk=barcodeID).update(
            status=False
        )

        return redirect(to='bookingView')




class BookingEdit(View):
    booking_forms = BookVehicleForm
    booking_model = booking.BookVehicle
    parking_model = parking_slot.Parking_slot
    # booking_add_templates = 'dashboard/bookingAdd.html'
    booking_edit_templates = 'dashboard/bookingEdit.html'

    def get_data(self, request, *args, **kwargs):
        if 'barcode_details' in kwargs:
            data = vehicle_details.VehicleDetail.objects.filter(pk=request.POST.get('barcode_details')).values(
                'barcode_number', 'vehicle_number', 'chessis_number', 'vehicle_model', 'variants', 'color',
                'status'
            )
            #     .annotate(
            #     client_booking_date=ExpressionWrapper(Func(F('date'), Value("DD/MM/YYYY"), function='TO_CHAR'),
            #                                     output_field=CharField()),
            # )



            return list(data)

    def get(self, request, *args, **kwargs):
        if 'BookingEdit' in kwargs:
            model = self.booking_model.objects.get(id=kwargs.get('object_id'))
            editform = self.booking_forms(instance=model)
            return render(request, self.booking_edit_templates, {'form': editform})

    def post(self, request, *args, **kwargs):

        if 'barcode_details' in kwargs:
            data = self.get_data(request, barcode_details='')
            # print(data)
            return JsonResponse(data, safe=False)

        forms = self.booking_forms(request.POST or None)
        # parkingID = request.POST['slot']
        # selected_slot = self.parking_model.objects.get(pk=parkingID)
        if forms.is_valid():
            barcode_details = forms.cleaned_data.get('barcode_details')
            vehicle_no = forms.cleaned_data.get('vehicle_no')
            chessis_no = forms.cleaned_data.get('chessis_no')
            vehicle_model = forms.cleaned_data.get('vehicle_model')
            variants = forms.cleaned_data.get('variants')
            color = forms.cleaned_data.get('color')
            # booking_date = forms.cleaned_data.get('booking_date')
            # parking_slot = forms.cleaned_data.get('parking_slot')
            data = self.booking_model.objects.filter(id=kwargs.get('object_id')).update(barcode_details=barcode_details,
                                                                                        vehicle_no=vehicle_no,
                                                                                        chessis_no=chessis_no,
                                                                                        vehicle_model=vehicle_model,
                                                                                        variants=variants, color=color)

            # self.parking_model.objects.filter(pk=parkingID).update(
            #     slot_status=False
            # )

            return redirect(to='bookingView')


class Exit(View):
    booking_model = booking.BookVehicle
    exit_forms = ExitVehicleForm
    parking_model = parking_slot.Parking_slot
    exit_model = booking.ParkingExit
    exit_add_templates = 'dashboard/ExitAdd.html'
    exit_view_templates = 'dashboard/exitView.html'

    def get(self, request, *args, **kwargs):
        if 'exit' in kwargs:
            # model=self.exit_model.objects.all()
            available_barcode_no = self.booking_model.objects.filter(status=True)
            # print(available_barcode_no)
            return render(request, self.exit_add_templates,
                          {'form': self.exit_forms(), 'available_barcode': available_barcode_no})

        elif 'exitView' in kwargs:
            model = self.exit_model.objects.all().order_by('-id').annotate(
                client_exit_date=ExpressionWrapper(Func(F('exit_date'), Value("DD/MM/YYYY"), function='TO_CHAR'),
                              output_field=CharField()),client_exit_time=ExpressionWrapper(Func(F('exit_date'), Value("HH24:MI:SS"), function='TO_CHAR'),
                              output_field=CharField()),


            )




            return render(request, self.exit_view_templates, {'form': model})

    def get_data(self, request, *args, **kwargs):
        if 'barcode_no' in kwargs:
            data = self.booking_model.objects.filter(pk=request.POST.get('barcode_no')).values(
                'barcode_details', 'vehicle_no', 'chessis_no', 'vehicle_model', 'variants', 'color'

            ).annotate(
                client_parking_slot=F('parking_slot__slot_name')
            )

            return list(data)

    def post(self, request, *args, **kwargs):
        forms = self.exit_forms(request.POST)
        if 'barcode_no' in kwargs:
            data = self.get_data(request, barcode_no='')
            return JsonResponse(data, safe=False)

        barcodeID = request.POST['barcode']
        selected_barcode = self.booking_model.objects.get(pk=barcodeID)
        vehicle_no = request.POST['vehicle_no']
        chessis_no = request.POST['chessis_no']
        vehicle_model = request.POST['vehicle_model']
        variants = request.POST['variants']
        color = request.POST['color']
        parking_slot = request.POST['parking_slot']
        exit_data = self.exit_model.objects.create(barcode=selected_barcode, vehicle_no=vehicle_no,
                                                   chessis_no=chessis_no, vehicle_model=vehicle_model
                                                   , variants=variants, color=color, slot=parking_slot)

        update_slot = self.parking_model.objects.filter(slot_name=parking_slot).update(
            slot_status=True
        )

        return redirect(to='exitView')



class LiveTracking(View):
    booking_model = booking.BookVehicle

    exit_model = booking.ParkingExit
    # exit_model1 = booking.parkingExit
    live_vehicle_templates = "dashboard/liveVehicle.html"

    def get(self, request, *args, **kwargs):
        if 'liveTracking' in kwargs:
            entry_entry_data = self.booking_model.objects.values('vehicle_no', 'chessis_no',
                                                                 'vehicle_model', 'variants', 'color', 'booking_date'
                                                                 ).annotate(
                client_parking_slot=F('parking_slot__slot_name'),
                client_selected_barcode=F('barcode_details__barcode_number'),
                # bn=F('parkingexit__exit_date')
                client_entry_date=ExpressionWrapper(Func(F('booking_date'), Value("DD/MM/YYYY"), function='TO_CHAR'),
                              output_field=CharField()),client_entry_time = ExpressionWrapper(
                Func(F('booking_date'), Value("HH24:MI:SS"), function='TO_CHAR'),
                output_field=CharField()),

                client_exit_date=ExpressionWrapper(Func(F('parkingexit__exit_date'), Value("DD/MM/YYYY"), function='TO_CHAR'),
                              output_field=CharField()), client_exit_time = ExpressionWrapper(
                Func(F('parkingexit__exit_date'), Value("HH24:MI:SS"), function='TO_CHAR'),
                output_field=CharField()),

            # bn = Coalesce('parkingexit__exit_date', V("-")),
            ) \
                .order_by('-id') \
                .distinct()

            return render(request, self.live_vehicle_templates,
                          {'form': entry_entry_data})


class CategoryAdd(View):
    category_forms = CategoryForm
    category_model = category.Category
    category_add_templates = 'dashboard/categoryAdd.html'
    category_view_templates = 'dashboard/categoryView.html'

    def get(self, request, *args, **kwargs):
        if 'category' in kwargs:
            return render(request, self.category_add_templates, {'form': self.category_forms()})

        elif 'categoryView' in kwargs:
            model = self.category_model.objects.all()
            # print(model)
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


class CategoryEdit(View):
    category_forms = CategoryForm
    category_model = category.Category
    category_edit_templates = 'dashboard/categoryEdit.html'

    def get(self, request, *args, **kwargs):
        if 'categoryEdit' in kwargs:
            editmodel = self.category_model.objects.get(id=kwargs.get('object_id'))
            editform = self.category_forms(instance=editmodel)
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


# ------------------new


class BookVehicle(View):
    vehicle_forms = UserVehicleForm
    vehicle_model = add_vehicle.UserVehicle
    parking_model = parking_slot.Parking_slot
    bookVehicle_add_templates = 'dashboard/add_vehicle.html'
    bookVehicle_view_mplates = 'dashboard/view_vehicle.html'

    def get(self, request, *args, **kwargs):
        if 'bookVehicle' in kwargs:
            available_slot = parking_slot.Parking_slot.objects.filter(slot_status=True)
            return render(request, self.bookVehicle_add_templates,
                          {'form': self.vehicle_forms(), 'available_slot': available_slot})


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
            self.vehicle_model.objects.create(categoty_name=categoty_name, Barcode_no=Barcode_no, owner_name=owner_name,
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
            editForm = self.vehicle_forms(instance=editmodel)
            return render(request, self.bookVehicle_edit_mplates,
                          {'UpdateVehicle': editForm, 'available_slot': available_slot})

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
            self.vehicle_model.objects.filter(id=kwargs.get('object_id')).update(categoty_name=categoty_name,
                                                                                 Barcode_no=Barcode_no,
                                                                                 owner_name=owner_name,
                                                                                 owner_contact=owner_contact,
                                                                                 vehicle_model=vehicle_model,
                                                                                 vehicle_no=vehicle_no,
                                                                                 chessis_no=chessis_no,
                                                                                 parking_slot=parking_slot)
            # messages.success(request, 'successfully add to database ')
            # self.parking_model.objects.filter(pk=parkingID).update(
            #     slot_status=False
            # )
            return redirect(to='viewVehicle')


# ----------------------------end old
class ParkingEntry(View):
    parking_entry_forms = ParkingEntryForm
    parking_entry_model = parking_in.ParkingIn
    parking_entry_add_templates = 'dashboard/parking_entry.html'
    vehicle_model = add_vehicle.UserVehicle

    parking_entry_view_templates = 'dashboard/parkingEntry_view.html'

    def get(self, request, *args, **kwargs):
        if 'parkingEntry' in kwargs:
            available_barcode = add_vehicle.UserVehicle.objects.filter(status=True)
            return render(request, self.parking_entry_add_templates,
                          {'form': self.parking_entry_forms(), 'barcode': available_barcode})
        elif 'parkingEntryView' in kwargs:
            model = self.parking_entry_model.objects.all()
            return render(request, self.parking_entry_view_templates, {'parkingView': model})

    # def get(self, request, *args, **kwargs):
    #     if 'parkingEntry' in kwargs:
    #         available_barcode = add_vehicle.UserVehicle.objects.all()
    #         return render(request, self.parking_entry_add_templates, {'form': self.parking_entry_add_templates,'barcode':available_barcode})

    def post(self, request, *args, **kwargs):
        barcode = request.POST['barcode']
        # print(barcode)
        entrydate = request.POST['entrydate']
        entrytime = request.POST['entrytime']
        barcode_no = add_vehicle.UserVehicle.objects.get(pk=barcode)

        entrysave = parking_in.ParkingIn.objects.create(
            user_details=barcode_no, entry_date=entrydate, entry_time=entrytime)
        barcode_no = self.vehicle_model.objects.get(pk=barcode)
        # print(barcode_no)
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
    parking_entry_forms = ParkingEntryForm
    parking_entry_model = parking_in.ParkingIn
    parking_entry_edit_templates = 'dashboard/parkingEntry_edit.html'

    def get(self, request, *args, **kwargs):
        if 'parkingEntryEdit' in kwargs:
            editmodel = self.parking_entry_model.objects.get(id=kwargs.get('object_id'))
            editForm = self.parking_entry_forms(instance=editmodel)
            return render(request, self.parking_entry_edit_templates, {'UpdateparkingEntry': editForm})

    def post(self, request, *args, **kwargs):
        forms = self.parking_entry_forms(request.POST)
        if forms.is_valid():
            user_details = forms.cleaned_data.get('user_details')
            entry_date = forms.cleaned_data.get('entry_date')
            entry_time = forms.cleaned_data.get('entry_time')
            self.parking_entry_model.objects.filter(id=kwargs.get('object_id')).update(
                user_details=user_details, entry_date=entry_date, entry_time=entry_time)
            return redirect(to='parkingEntryView')


class ParkingExit(View):
    parking_exit_forms = ParkingOutForm
    parking_exit_model = parkingOut.ParkingOut
    parking_exit_add_templates = 'dashboard/parkingOutAdd.html'
    parking_exit_view_templates = 'dashboard/parkingExit_view.html'

    def get(self, request, *args, **kwargs):
        if 'parkingExit' in kwargs:
            available_barcode = add_vehicle.UserVehicle.objects.filter(status=False)
            return render(request, self.parking_exit_add_templates,
                          {'form': self.parking_exit_forms(), 'barcode': available_barcode})
        elif 'parkingExitView' in kwargs:
            model = self.parking_exit_model.objects.all()
            return render(request, self.parking_exit_view_templates, {'parkingExitView': model})

    def post(self, request, *args, **kwargs):
        barcode = request.POST['barcode']
        exitdate = request.POST['exitdate']
        exittime = request.POST['exittime']
        barcode_no = add_vehicle.UserVehicle.objects.get(pk=barcode)

        exitsave = parkingOut.ParkingOut.objects.create(
            user_details=barcode_no, exit_date=exitdate, exit_time=exittime)

        # add_vehicle.UserVehicle.objects.filter(id=barcode).update(
        #     status=True
        # )
        return redirect(to='parkingExit')
