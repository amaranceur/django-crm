from django.urls import path
from .views import *
urlpatterns = [
    path('',home,name="home"),
    # path('login/',,name="login"),
    path('logout/',logout_user,name='logout'),
    path('register/',register_user,name='register'),
    path('add_record',add_record,name='Add_record'),
    path('record/<int:pk>',costumer_record,name='record'),
    path('delete_record/<int:pk>',delete_record,name='delete_record'),
    path('update_record/<int:pk>',update_record,name='update_record')
]

