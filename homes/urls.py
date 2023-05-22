from django.urls import path
from homes import views


urlpatterns = [
    ## home list
    path('', views.HomeAPI.as_view()),

    
    ## home set
    path('general_setting/<str:home_id>/<str:type>/', views.HomeGeneralSettingsAPI.as_view()),

    ## Admin
    path('', views.HomeAdminAPI.as_view())
]