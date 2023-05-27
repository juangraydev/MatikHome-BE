from django.urls import path
from homes import views


urlpatterns = [

    
    ## Room APIs
    ## [PUT] [POST]
    path('room/', views.RoomAPI.as_view()),
    ##  [DELETE]
    path('room/<str:room_id>/', views.RoomAPI.as_view()),

    
    ## Home APIs
    ## [GET] [POST] [PUT]
    path('', views.HomeAPI.as_view()),
    ## [DELETE]
    path('<str:home_id>/', views.HomeAPI.as_view()),





    ## home list
    # path('<str:home_id>/', views.HomeAPI.as_view()),

    
    # path('room/<str:room_id>/', views.RoomAPI.as_view()),

    
    ## home set
    # path('general_setting/<str:home_id>/<str:type>/', views.HomeGeneralSettingsAPI.as_view()),

    ## Admin
    # path('', views.HomeAdminAPI.as_view())
]