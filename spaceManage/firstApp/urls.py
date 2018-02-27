from django.urls import path
from firstApp import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'firstApp'

urlpatterns = [

path('',views.index,name='index'),
path('index/',views.index,name='index'),
path('signup/',views.signup,name='signup'),
path('userlogin/',views.userlogin,name='userlogin'),
path('webgl/',views.webgl,name='')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
