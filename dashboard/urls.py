from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('vehicle', views.Vehicle.as_view(),{'vehicle':''}, name='vehicle'),
    path('vehicleView', views.Vehicle.as_view(),{'vehicleView':''}, name='vehicleView'),

    # path('vehicle_excel',views.VehicleExcel.as_view(),{'vehicle_excel':''},name='vehicle_excel'),
    path('register', views.RegisterPage.as_view(), {'register': ''}, name='register'),

    # path('register', views.register, name='register'),
    path('dashboard', views.Dashboard.as_view(), {'dashboard': ''}, name='dashboard'),

    path('', views.LoginPage.as_view(), {'login': ''}, name='login'),

    # path('category', views.Category.as_view(), {'category': ''}, name='category'),
    path('categoryView', views.CategoryAdd.as_view(), {'categoryView': ''}, name='categoryView'),
    path('category', views.CategoryAdd.as_view(), {'category': ''}, name='category'),
    path('categoryEdit/<int:object_id>', views.CategoryEdit.as_view(), {'categoryEdit': ''}, name="categoryEdit"),

    path('exit', views.Exit.as_view(), {'exit': ''}, name='exit'),
    path('barcode_no', views.Exit.as_view(), {'barcode_no': ''}, name='barcode_no'),

    path('booking', views.Booking.as_view(), {'booking': ''}, name='booking'),
    path('bookingView', views.Booking.as_view(), {'bookingView': ''}, name='bookingView'),
    path('barcode_details', views.Booking.as_view(), {'barcode_details': ''}, name='barcode_details'),
    path('BookingEdit/<int:object_id>', views.BookingEdit.as_view(), {'BookingEdit': ''}, name='BookingEdit'),

    path('bookVehicle', views.BookVehicle.as_view(), {'bookVehicle': ''}, name='bookVehicle'),
    path('viewVehicle', views.BookVehicle.as_view(), {'viewVehicle': ''}, name='viewVehicle'),
    path('EditVehicle/<int:object_id>', views.EditVehicle.as_view(), {'EditVehicle': ''}, name="EditVehicle"),
    path('deleteVehicle/<int:object_id>', views.BookVehicle.as_view(), {'viewVehicle': ''}, name='viewVehicle'),

    path('parkingSlot', views.ParkingSlot.as_view(), {'parkingSlot': ''}, name='parkingSlot'),
    path('parkingSlotView', views.ParkingSlot.as_view(), {'parkingSlotView': ''}, name='parkingSlotView'),
    path('parkingSlotEdit/<int:object_id>', views.ParkingSlotEdit.as_view(), {'parkingSlotEdit': ''}, name="parkingSlotEdit"),

    path('parkingEntry',views.ParkingEntry.as_view(),{'parkingEntry':''},name='parkingEntry'),
    path('parkingEntryView',views.ParkingEntry.as_view(),{'parkingEntryView':''},name='parkingEntryView'),
    path('parkingEntryEdit/<int:object_id>',views.ParkingEntryEdit.as_view(),{'parkingEntryEdit':''},name='parkingEntryEdit'),

    path('parkingExit', views.ParkingExit.as_view(), {'parkingExit': ''}, name='parkingExit'),
    path('parkingExitView', views.ParkingExit.as_view(), {'parkingExitView': ''}, name='parkingExitView'),

]
