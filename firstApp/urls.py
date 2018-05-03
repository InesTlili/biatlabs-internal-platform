from django.urls import path
from firstApp import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.DefaultRouter()
router.register('visitors', views.VisitorViewSet)


app_name = 'firstApp'

urlpatterns = [

path('',views.index2,name='index2'),
path('index/',views.index,name='index'),
path('signup/',views.signup,name='signup'),
path('userlogin/',views.userlogin,name='userlogin'),
path('webgl/',views.webgl,name=''),
path('api/visitors',views.visitors_list,name="api/visitors")
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
