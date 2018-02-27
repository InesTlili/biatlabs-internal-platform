"""spaceManage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from firstApp import views
from django.conf.urls import include

urlpatterns = [

    path('',views.index,name='index'),
    path('',include('firstApp.urls')),
    path('admin/', admin.site.urls),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('special/',views.special,name='special'),
    path('reserve/',views.reserve,name='reserve'),
    path('reservations/',views.reservations,name='reservations'),
    path('adminhome/',views.admin,name='admin'),
    path('delete/<reservation_id>',views.deletereserv,name='delete'),
    path('validate/<reservation_id>',views.validate,name='validate'),
    path('validateuser/<user_id>',views.validateuser,name='validateuser'),
    path('deleteuser/<user_id>',views.deleteuser,name='deleteuser'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('notes/',views.notespage,name='notes'),
    path('validation/users',views.adminusers,name='adminusers'),
    path('validation/reservations',views.adminreservations,name='adminreservations'),
        #path('edit/<reservation_id>',views.editreserv,name='edit'),
    path('base2/',views.try2,name='base2'),
    path('getcourse/<course_id>',views.getcourse,name='getcourse'),
    path('dashplot/',views.dashplot,name='dashplot')


]
