from django.urls import path
from admin import views


urlpatterns = [
    ## Admin API
    # path('summary/', views.HomeAPI.as_view()),
    path('users/', views.UserListAPI.as_view()),
    path('homes/', views.HomeListAPI.as_view()),
    # path('device/', views.HomeAPI.as_view()),
]