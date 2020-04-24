from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('vehicle', views.vehicle, name='vehicle'),
    path('register', views.register, name='register'),
    # path('Dashboard', views.Dashboard, name='dashboard'),
    path('dashboard', views.Dashboard.as_view(), {'dashboard': ''}, name='dashboard'),

    path('', views.LoginPage.as_view(), {'login': ''}, name='login'),

    path('category', views.Category.as_view(), {'category': ''}, name='category'),
    path('categoryView', views.Category.as_view(), {'categoryView': ''}, name='categoryView'),
    path('categoryEdit/<int:object_id>', views.CategoryEdit.as_view(), {'categoryEdit': ''}, name="categoryEdit"),

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
