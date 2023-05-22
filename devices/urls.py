from django.urls import path
from devices import views

urlpatterns = [
    ## login
    path('', views.DeviceAPI.as_view(), name="device"),
    path('key/', views.DeviceESPAPI.as_view(), name="device_by_key"),

]