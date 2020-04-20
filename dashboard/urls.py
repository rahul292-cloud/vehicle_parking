from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category', views.Category.as_view(), {'category': ''}, name='category'),
    path('bookVehicle', views.BookVehicle.as_view(), {'bookVehicle': ''}, name='bookVehicle'),
    path('viewVehicle', views.BookVehicle.as_view(), {'viewVehicle': ''}, name='viewVehicle'),
    path('deleteVehicle/<int:id>', views.BookVehicle.as_view(), {'viewVehicle': ''}, name='viewVehicle'),
    path('parkingSlot', views.ParkingSlot.as_view(), {'parkingSlot': ''}, name='parkingSlot'),
    path('parkingEntry',views.ParkingEntry.as_view(),{'parkingEntry':''},name='parkingEntry')
]
