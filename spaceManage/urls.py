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
from rest_framework import routers


router = routers.DefaultRouter()
router.register('/visitors', views.VisitorViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('',views.index2,name='index2'),
    path('',include('firstApp.urls')),
    path('admin/', admin.site.urls),
    path('userlogout/',views.userlogout,name='userlogout'),
    path('special/',views.special,name='special'),
    path('reserve/room',views.reserve,name='reserve'),
    path('reserve/locker',views.reservelocker,name='reserve/locker'),
    path('reservations/',views.reservations,name='reservations'),

    path('home/',views.home,name='home'),

    path('delete/<reservation_id>',views.deletereserv,name='delete'),
    path('validate/<reservation_id>',views.validate,name='validate'),

    path('validateuser/<user_id>',views.validateuser,name='validateuser'),
    path('deleteuser/<user_id>',views.deleteuser,name='deleteuser'),

    path('userlogin/',views.userlogin,name='userlogin'),

    path('notes/',views.notespage,name='notes'),
    path('deletenote/<note_id>',views.deletenote,name='deletenote'),


    path('validation/users',views.adminusers,name='adminusers'),
    path('validation/reservations',views.adminreservations,name='adminreservations'),
    path('validation/lockers',views.adminlockers,name='adminlockers'),
    path('makepresence',views.makepresence,name='makepresence'),

    path('deletelocker/<locker_id>',views.deletelocker,name='deletelocker'),
    path('validatelocker/<locker_id>',views.validatelockers,name='validatelockers'),
        #path('edit/<reservation_id>',views.editreserv,name='edit'),
    path('base2/',views.try2,name='base2'),
    path('getcourse/<course_id>',views.getcourse,name='getcourse'),
    path('oc/getcourse/<course_id>',views.getcourse2,name='oc/getcourse'),
    path('dashplot/',views.dashplot,name='dashplot'),

    path('lockers/',views.reservelocker,name='lockers'),
    path('alllockers/',views.lockers,name='alllockers'),

    path('visualize/users',views.seeusers,name='seeusers'),
    path('visualize/reservations',views.seereservations,name='seereservations'),
    path('visualize/notes',views.seenotes,name='seenotes'),
    path('visualize/lockers',views.seelockers,name='seelockers'),
    path('visualize/visitors',views.seevisitors,name='seevisitors'),

    path('api/visitors',views.visitors_list,name="api/visitors"),
    path('api/chairs',views.chairs_list,name="api/chairs"),

    path('stats/presence',views.stats_presence,name="stats/presence"),
    path('stats/reservation',views.stats_reservation,name="stats/reservation"),

    path('test',views.test,name="test"),

    path('add/workshop',views.add_workshop,name='add/workshop'),
    path('workshops',views.workshops,name='workshops'),

    path('validatewks/<workshop_id>',views.validatewks,name='validatewks'),
    path('deletewks/<workshop_id>',views.deletewks,name='deletewks'),
    path('presencewks/<workshop_id>',views.presencewks,name='presencewks'),
    path('addwkspresence/<workshop_id>/<startup_id>',views.addwkspresence,name='addwkspresence'),

    path('myworkshops',views.myworkshops,name='myworkshops'),

    path('evaluate/<startup_id>',views.evaluate,name='evaluate'),
    path('oc',views.getoc,name='oc'),
    path('objectives/<startup_id>/<week>',views.objectives,name='objectives'),
    path('objectiveDone/<obj_id>/<startup_id>/<week>',views.objectiveDone,name='objectiveDone'),
    path('startups',views.stpredirect,name='startups'),
    path('profile/<user_id>',views.profile,name='profile'),
    path('main',views.main,name='main'),
    path('startups-portal',views.stport,name='startupsp')

]
