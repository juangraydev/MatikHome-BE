from django.urls import path
from devices import views

urlpatterns = [
    path('', views.DeviceAPI.as_view(), name="device"),
    path('<uuid:home_id>/', views.DeviceHomeAPI.as_view(), name="home_device"),
    path('key/', views.DeviceESPAPI.as_view(), name="device_by_key"),

]