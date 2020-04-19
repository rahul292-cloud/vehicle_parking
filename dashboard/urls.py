from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category', views.Category.as_view(), {'category': ''}, name='category'),
    path('bookVehicle', views.BookVehicle.as_view(), {'bookVehicle': ''}, name='bookVehicle'),
    path('parkingSlot', views.ParkingSlot.as_view(), {'parkingSlot': ''}, name='parkingSlot'),
]
