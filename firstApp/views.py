from django.shortcuts import render
from datetime import timedelta
import datetime
import time

from firstApp.models import Objective,UserInfo, Reservation,Need,Module,Content,Course,Locker,Postit,Visitor,Startup,Presence,Chair,Workshop,Evaluation
from . import forms
from firstApp.forms import PassForm,UserForm,ProfileForm,reserve,needform,postitform,presenceform,addworkshop,evaluationform,objectiveform

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required



from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


import plotly.plotly as py
import plotly.figure_factory as ff
import plotly

from rest_framework import status,viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

from django.http import JsonResponse
from graphos.sources.model import ModelDataSource
from graphos.renderers import flot
from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
from django.db.models import Avg

# Create your views here.

class VisitorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows visitors to be viewed or edited.
    """
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer

@api_view(['GET', 'POST'])
def visitors_list(request):
    if request.method == 'GET':
        visitors = Visitor.objects.all()
        serializer = VisitorSerializer(visitors,context={'request': request} ,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VisitorSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChairViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows presences to be viewed or edited.
    """
    queryset = Chair.objects.all()
    serializer_class = ChairSerializer

@api_view(['GET', 'POST'])
def chairs_list(request):
    if request.method == 'GET':
        chairs = Chair.objects.all()
        serializer = ChairSerializer(chairs,context={'request': request} ,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ChairSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.data)

        print("it's getting here")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def try2(request):
    modules= Module.objects.filter(isActive=False).order_by('number')
    courses=Course.objects.all()
    state=True


    return render(request,'base2.html',{'modules':modules,'courses':courses,'state':state})

def index2(request):
    return render(request,'index2.html')

def dashplot(request):
    rs=Reservation.objects.order_by('date','startTime').values()
    print(rs)
    df=[]
    for r in rs:
        us = User.objects.get(id=r['user_id'])
        if r['typeOf']=='Big meeting room':
            resso='big'
        if r['typeOf']=='Small meeting room':
            resso='small'
        if r['typeOf']=='Training Room':
            resso='training'

        df.append(dict(Task=resso,Start=str(r['date'])+str(' ')+str(r['startTime']), Finish=str(r['date'])+str(' ')+str(r['endTime']), Resource=us.username,))

    colors = dict(big = 'rgb(46, 137, 205)',
                  small = 'rgb(114, 44, 121)',
                  training = 'rgb(198, 47, 105)',
                  Brain = 'rgb(58, 149, 136)',
                  Rest = 'rgb(107, 127, 135)')

    fig = ff.create_gantt(df, index_col='Resource', title='Daily Schedule', group_tasks=True,
                          show_colorbar=True,showgrid_x=True, showgrid_y=True )
                          #bar_width=0.8, showgrid_x=True, showgrid_y=True
    plotly.offline.plot(fig, filename='gantt-hours-minutes')
    return render(request,'dashplot.html')

def getcourse(request, course_id=None):
    cont=Content.objects.get(course=course_id)
    course=Course.objects.get(id=course_id)
    modules= Module.objects.order_by('number')
    courses=Course.objects.all()
    st=True
    st2=True
    st3=True
    v = True
    v2 = True
    v3 = True
    v4 = True

    if cont.videoURL==None:
        v=False
    if cont.videoURL2==None:
        v2=False
    if cont.videoURL3==None:
        v3=False
    if cont.videoURL4==None:
        v4=False
    if cont.articleURL==None:
        st=False
    if cont.articleURL2==None:
        st2=False
    if cont.articleURL3==None:
        st3=False

    return render(request,'course.html',{'cont':cont,'modules':modules,'courses':courses,'course':course,'st':st,'st2':st2,'st3':st3,'v':v,'v2':v2,'v3':v3,'v4':v4})

def getcourse2(request, course_id=None):
    cont=Content.objects.get(course=course_id)
    course=Course.objects.get(id=course_id)
    modules= Module.objects.filter(isActive=True).order_by('number')
    courses=Course.objects.all()
    st=True
    st2=True
    st3=True
    v = True
    v2 = True
    v3 = True
    v4 = True
    if cont.videoURL==None:
        v=False
    if cont.videoURL2==None:
        v2=False
    if cont.videoURL3==None:
        v3=False
    if cont.videoURL4==None:
        v4=False
    if cont.articleURL==None:
        st=False
    if cont.articleURL2==None:
        st2=False
    if cont.articleURL3==None:
        st3=False
    #return HttpResponseRedirect(reverse('home'))

    return render(request,'course2.html',{'cont':cont,'modules':modules,'courses':courses,'course':course,'st':st,'st2':st2,'st3':st3,'v':v,'v2':v2,'v3':v3,'v4':v4})


def index(request):
    return render(request, 'index.html')

#def adminhome(request):
#    users=User.objects.order_by('fullName')
#    myDict = {'users_list' : users}
#    return render(request, 'adminhome.html',context=myDict)

def webgl(request):
    return render(request,'newLogic/index.html')

def signup(request):

    registered=False
    if request.method=='POST':
        Userform = UserForm(data=request.POST)
        Profileform = ProfileForm(request.POST, request.FILES)
        if Userform.is_valid() and Profileform.is_valid():
            user=Userform.save(commit=False)
            user.set_password(user.password)
            user.is_active=False
            user.save()
            print("1")
            profile=Profileform(profilePic=request.FILES('profilePic')).save(commit=False)
            print("2")

            profile.user=user
            profile.save()



            return HttpResponse('We will send you an email as soon as your account gets activated !')
            registered=True

        else :
            print(Userform.errors,Profileform.errors)

    else :
        Userform=UserForm()
        Profileform=ProfileForm()

    return render(request,'register.html',{'Userform':Userform,'Profileform':Profileform,'registered':registered})

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                #if user.is_staff:
                #    login(request,user)
                #    return HttpResponseRedirect(reverse('admin'))
                #else:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else :
                return HttpResponse("Account not active !")

        else :
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Login Failed Successfully ! :D")
    else:
        return render(request,'index2.html',{})

@login_required
def userlogout(request):
        logout(request)
        return HttpResponseRedirect(reverse('index2'))

@login_required
def special(request):
    return HttpResponse("You are logged in, nice ! :-)")

@login_required
def reserve(request):
    reservationform= forms.reserve()
    res_list = Reservation.objects.order_by('space')
    message = ""
    trcolor1="blue"
    trcolor2="blue"
    trcolor3="blue"
    trcolor4="blue"
    trcolor5="blue"
    trcolor6="blue"
    trcolor7="blue"
    trcolor8="blue"
    trcolor9="blue"
    trcolor10="blue"
    trcolor11="blue"
    trcolor12="blue"
    trcolor13="blue"
    trcolor14="blue"
    trcolor15="blue"
    trcolor16="blue"
    trcolor17="blue"
    trcolor18="blue"
    trcolor19="blue"
    trcolor20="blue"
    trcolor21="blue"
    trcolor22="blue"
    trcolor23="blue"
    trcolor24="blue"
    trcolor25="blue"
    trcolor26="blue"
    trcolor27="blue"
    trcolor28="blue"
    trcolor29="blue"
    trcolor30="blue"
    trcolor31="blue"
    trcolor32="blue"
    trcolor33="blue"
    trcolor34="blue"
    trcolor35="blue"
    trcolor36="blue"
    trcolor37="blue"
    trcolor38="blue"
    trcolor39="blue"
    trcolor40="blue"
    trcolor41="blue"
    trcolor42="blue"
    trcolor43="blue"
    trcolor44="blue"
    trcolor45="blue"
    trcolor46="blue"
    trcolor47="blue"
    trcolor48="blue"



    smrcolor1="blue"
    smrcolor2="blue"
    smrcolor3="blue"
    smrcolor4="blue"
    smrcolor5="blue"
    smrcolor6="blue"
    smrcolor7="blue"
    smrcolor8="blue"
    smrcolor9="blue"
    smrcolor10="blue"
    smrcolor11="blue"
    smrcolor12="blue"
    smrcolor13="blue"
    smrcolor14="blue"
    smrcolor15="blue"
    smrcolor16="blue"
    smrcolor17="blue"
    smrcolor18="blue"
    smrcolor19="blue"
    smrcolor20="blue"
    smrcolor21="blue"
    smrcolor22="blue"
    smrcolor23="blue"
    smrcolor24="blue"
    smrcolor25="blue"
    smrcolor26="blue"
    smrcolor27="blue"
    smrcolor28="blue"
    smrcolor29="blue"
    smrcolor30="blue"
    smrcolor31="blue"
    smrcolor32="blue"
    smrcolor33="blue"
    smrcolor34="blue"
    smrcolor35="blue"
    smrcolor36="blue"
    smrcolor37="blue"
    smrcolor38="blue"
    smrcolor39="blue"
    smrcolor40="blue"
    smrcolor41="blue"
    smrcolor42="blue"
    smrcolor43="blue"
    smrcolor44="blue"
    smrcolor45="blue"
    smrcolor46="blue"
    smrcolor47="blue"
    smrcolor48="blue"


    bmrcolor1="blue"
    bmrcolor2="blue"
    bmrcolor3="blue"
    bmrcolor4="blue"
    bmrcolor5="blue"
    bmrcolor6="blue"
    bmrcolor7="blue"
    bmrcolor8="blue"
    bmrcolor9="blue"
    bmrcolor10="blue"
    bmrcolor11="blue"
    bmrcolor12="blue"
    bmrcolor13="blue"
    bmrcolor14="blue"
    bmrcolor15="blue"
    bmrcolor16="blue"
    bmrcolor17="blue"
    bmrcolor18="blue"
    bmrcolor19="blue"
    bmrcolor20="blue"
    bmrcolor21="blue"
    bmrcolor22="blue"
    bmrcolor23="blue"
    bmrcolor24="blue"
    bmrcolor25="blue"
    bmrcolor26="blue"
    bmrcolor27="blue"
    bmrcolor28="blue"
    bmrcolor29="blue"
    bmrcolor30="blue"
    bmrcolor31="blue"
    bmrcolor32="blue"
    bmrcolor33="blue"
    bmrcolor34="blue"
    bmrcolor35="blue"
    bmrcolor36="blue"
    bmrcolor37="blue"
    bmrcolor38="blue"
    bmrcolor39="blue"
    bmrcolor40="blue"
    bmrcolor41="blue"
    bmrcolor42="blue"
    bmrcolor43="blue"
    bmrcolor44="blue"
    bmrcolor45="blue"
    bmrcolor46="blue"
    bmrcolor47="blue"
    bmrcolor48="blue"

    #Colors distribution
    for r in res_list :
        if r.isValidated:
                if r.date==datetime.date.today():
                    if r.typeOf=="Small meeting room":
                        if str(r.startTime)=="00:00:00":
                            smrcolor1="red"
                            if str(r.endTime)=="01:00:00":
                                smrcolor2="red"
                            if str(r.endTime)=="02:00:00":
                                smrcolor2="red"
                                smrcolor3="red"
                                smrcolor4="red"
                            if str(r.endTime)=="03:00:00":
                                smrcolor2="red"
                                smrcolor3="red"
                                smrcolor4="red"
                                smrcolor5="red"
                                smrcolor6="red"
                        elif str(r.startTime)=="00:30:00":
                            smrcolor2="red"
                            if str(r.endTime)=="01:30:00":
                                smrcolor3="red"
                            if str(r.endTime)=="2:30:00":
                                smrcolor3="red"
                                smrcolor4="red"
                                smrcolor5="red"
                            if str(r.endTime)=="3:30:00":
                                smrcolor7="red"
                                smrcolor3="red"
                                smrcolor4="red"
                                smrcolor5="red"
                                smrcolor6="red"
                        elif str(r.startTime)=="01:00:00":
                            smrcolor3="red"
                            if str(r.endTime)=="02:00:00":
                                smrcolor4="red"
                            if str(r.endTime)=="03:00:00":
                                smrcolor4="red"
                                smrcolor5="red"
                                smrcolor6="red"
                            if str(r.endTime)=="04:00:00":
                                smrcolor8="red"
                                smrcolor7="red"
                                smrcolor4="red"
                                smrcolor5="red"
                                smrcolor6="red"
                        elif str(r.startTime)=="01:30:00":
                            smrcolor4="red"
                            if str(r.endTime)=="02:30:00":
                                smrcolor5="red"
                            if str(r.endTime)=="03:30:00":
                                smrcolor5="red"
                                smrcolor6="red"
                                smrcolor7="red"
                            if str(r.endTime)=="04:30:00":
                                smrcolor5="red"
                                smrcolor6="red"
                                smrcolor7="red"
                                smrcolor8="red"
                                smrcolor9="red"
                        elif str(r.startTime)=="02:00:00":
                            smrcolor5="red"
                            if str(r.endTime)=="03:00:00":
                                smrcolor6="red"
                            if str(r.endTime)=="04:00:00":
                                smrcolor6="red"
                                smrcolor7="red"
                                smrcolor8="red"
                            if str(r.endTime)=="05:00:00":
                                smrcolor10="red"
                                smrcolor6="red"
                                smrcolor7="red"
                                smrcolor8="red"
                                smrcolor9="red"
                        elif str(r.startTime)=="02:30:00":
                            smrcolor6="red"
                            if str(r.endTime)=="03:30:00":
                                smrcolor7="red"
                            if str(r.endTime)=="04:30:00":
                                smrcolor9="red"
                                smrcolor7="red"
                                smrcolor8="red"
                            if str(r.endTime)=="05:30:00":
                                smrcolor10="red"
                                smrcolor11="red"
                                smrcolor7="red"
                                smrcolor8="red"
                                smrcolor9="red"
                        elif str(r.startTime)=="03:00:00":
                            smrcolor7="red"
                            if str(r.endTime)=="04:00:00":
                                smrcolor8="red"
                            if str(r.endTime)=="05:00:00":
                                smrcolor9="red"
                                smrcolor10="red"
                                smrcolor8="red"
                            if str(r.endTime)=="06:00:00":
                                smrcolor10="red"
                                smrcolor11="red"
                                smrcolor12="red"
                                smrcolor8="red"
                                smrcolor9="red"
                        elif str(r.startTime)=="03:30:00":
                            smrcolor8="red"
                            if str(r.endTime)=="04:30:00":
                                smrcolor9="red"
                            if str(r.endTime)=="05:30:00":
                                smrcolor9="red"
                                smrcolor10="red"
                                smrcolor11="red"
                            if str(r.endTime)=="06:30:00":
                                smrcolor10="red"
                                smrcolor11="red"
                                smrcolor12="red"
                                smrcolor13="red"
                                smrcolor9="red"
                        elif str(r.startTime)=="04:00:00":
                            smrcolor9="red"
                            if str(r.endTime)=="05:00:00":
                                smrcolor10="red"
                            if str(r.endTime)=="06:00:00":
                                smrcolor12="red"
                                smrcolor10="red"
                                smrcolor11="red"
                            if str(r.endTime)=="07:00:00":
                                smrcolor10="red"
                                smrcolor11="red"
                                smrcolor12="red"
                                smrcolor13="red"
                                smrcolor14="red"
                        elif str(r.startTime)=="04:30:00":
                            smrcolor10="red"
                            if str(r.endTime)=="05:30:00":
                                smrcolor11="red"
                            if str(r.endTime)=="06:30:00":
                                smrcolor12="red"
                                smrcolor13="red"
                                smrcolor11="red"
                            if str(r.endTime)=="07:30:00":
                                smrcolor15="red"
                                smrcolor11="red"
                                smrcolor12="red"
                                smrcolor13="red"
                                smrcolor14="red"
                        elif str(r.startTime)=="05:00:00":
                            smrcolor11="red"
                            if str(r.endTime)=="06:00:00":
                                smrcolor12="red"
                            if str(r.endTime)=="07:00:00":
                                smrcolor12="red"
                                smrcolor13="red"
                                smrcolor14="red"
                            if str(r.endTime)=="08:00:00":
                                smrcolor15="red"
                                smrcolor16="red"
                                smrcolor12="red"
                                smrcolor13="red"
                                smrcolor14="red"
                        elif str(r.startTime)=="05:30:00":
                            smrcolor12="red"
                            if str(r.endTime)=="06:30:00":
                                smrcolor13="red"
                            if str(r.endTime)=="07:30:00":
                                smrcolor15="red"
                                smrcolor13="red"
                                smrcolor14="red"
                            if str(r.endTime)=="08:30:00":
                                smrcolor15="red"
                                smrcolor16="red"
                                smrcolor17="red"
                                smrcolor13="red"
                                smrcolor14="red"
                        elif str(r.startTime)=="06:00:00":
                            smrcolor13="red"
                            if str(r.endTime)=="07:00:00":
                                smrcolor14="red"
                            if str(r.endTime)=="08:00:00":
                                smrcolor15="red"
                                smrcolor16="red"
                                smrcolor14="red"
                            if str(r.endTime)=="09:00:00":
                                smrcolor15="red"
                                smrcolor16="red"
                                smrcolor17="red"
                                smrcolor18="red"
                                smrcolor14="red"
                        elif str(r.startTime)=="06:30:00":
                            smrcolor14="red"
                            if str(r.endTime)=="07:30:00":
                                smrcolor15="red"
                            if str(r.endTime)=="08:30:00":
                                smrcolor15="red"
                                smrcolor16="red"
                                smrcolor17="red"
                            if str(r.endTime)=="09:30:00":
                                smrcolor15="red"
                                smrcolor16="red"
                                smrcolor17="red"
                                smrcolor18="red"
                                smrcolor19="red"
                        elif str(r.startTime)=="07:00:00":
                            smrcolor15="red"
                            if str(r.endTime)=="08:00:00":
                                smrcolor16="red"
                            if str(r.endTime)=="09:00:00":
                                smrcolor18="red"
                                smrcolor16="red"
                                smrcolor17="red"
                            if str(r.endTime)=="10:00:00":
                                smrcolor20="red"
                                smrcolor16="red"
                                smrcolor17="red"
                                smrcolor18="red"
                                smrcolor19="red"
                        elif str(r.startTime)=="07:30:00":
                            smrcolor16="red"
                            if str(r.endTime)=="08:30:00":
                                smrcolor17="red"
                            if str(r.endTime)=="09:30:00":
                                smrcolor18="red"
                                smrcolor19="red"
                                smrcolor17="red"
                            if str(r.endTime)=="10:30:00":
                                smrcolor20="red"
                                smrcolor21="red"
                                smrcolor17="red"
                                smrcolor18="red"
                                smrcolor19="red"
                        elif str(r.startTime)=="08:00:00":
                            smrcolor17="red"
                            if str(r.endTime)=="09:00:00":
                                smrcolor18="red"
                            if str(r.endTime)=="10:00:00":
                                smrcolor18="red"
                                smrcolor19="red"
                                smrcolor20="red"
                            if str(r.endTime)=="11:00:00":
                                smrcolor20="red"
                                smrcolor21="red"
                                smrcolor22="red"
                                smrcolor18="red"
                                smrcolor19="red"
                        elif str(r.startTime)=="08:30:00":
                            smrcolor18="red"
                            if str(r.endTime)=="09:30:00":
                                smrcolor19="red"
                            if str(r.endTime)=="10:30:00":
                                smrcolor21="red"
                                smrcolor19="red"
                                smrcolor20="red"
                            if str(r.endTime)=="11:30:00":
                                smrcolor20="red"
                                smrcolor21="red"
                                smrcolor22="red"
                                smrcolor23="red"
                                smrcolor19="red"
                        elif str(r.startTime)=="09:00:00":
                            smrcolor19="red"
                            if str(r.endTime)=="10:00:00":
                                smrcolor20="red"
                            if str(r.endTime)=="11:00:00":
                                smrcolor21="red"
                                smrcolor22="red"
                                smrcolor20="red"
                            if str(r.endTime)=="12:00:00":
                                smrcolor20="red"
                                smrcolor21="red"
                                smrcolor22="red"
                                smrcolor23="red"
                                smrcolor24="red"
                        elif str(r.startTime)=="09:30:00":
                            smrcolor20="red"
                            if str(r.endTime)=="10:30:00":
                                smrcolor21="red"
                            if str(r.endTime)=="11:30:00":
                                smrcolor21="red"
                                smrcolor22="red"
                                smrcolor23="red"
                            if str(r.endTime)=="12:30:00":
                                smrcolor25="red"
                                smrcolor21="red"
                                smrcolor22="red"
                                smrcolor23="red"
                                smrcolor24="red"
                        elif str(r.startTime)=="10:00:00":
                            smrcolor21="red"
                            if str(r.endTime)=="11:00:00":
                                smrcolor22="red"
                            if str(r.endTime)=="12:00:00":
                                smrcolor24="red"
                                smrcolor22="red"
                                smrcolor23="red"
                            if str(r.endTime)=="13:00:00":
                                smrcolor25="red"
                                smrcolor26="red"
                                smrcolor22="red"
                                smrcolor23="red"
                                smrcolor24="red"
                        elif str(r.startTime)=="10:30:00":
                            smrcolor22="red"
                            if str(r.endTime)=="11:00:00":
                                smrcolor23="red"
                            if str(r.endTime)=="12:00:00":
                                smrcolor24="red"
                                smrcolor25="red"
                                smrcolor23="red"
                            if str(r.endTime)=="13:00:00":
                                smrcolor25="red"
                                smrcolor26="red"
                                smrcolor27="red"
                                smrcolor23="red"
                                smrcolor24="red"
                        elif str(r.startTime)=="11:00:00":
                            smrcolor23="red"
                            if str(r.endTime)=="11:00:00":
                                smrcolor24="red"
                            if str(r.endTime)=="12:00:00":
                                smrcolor24="red"
                                smrcolor25="red"
                                smrcolor26="red"
                            if str(r.endTime)=="13:00:00":
                                smrcolor25="red"
                                smrcolor26="red"
                                smrcolor27="red"
                                smrcolor28="red"
                                smrcolor24="red"
                        elif str(r.startTime)=="11:30:00":
                            smrcolor24="red"
                            if str(r.endTime)=="12:30:00":
                                smrcolor25="red"
                            if str(r.endTime)=="13:30:00":
                                smrcolor27="red"
                                smrcolor25="red"
                                smrcolor26="red"
                            if str(r.endTime)=="14:30:00":
                                smrcolor25="red"
                                smrcolor26="red"
                                smrcolor27="red"
                                smrcolor28="red"
                                smrcolor29="red"




                        elif str(r.startTime)=="12:00:00":
                            smrcolor25="red"
                            if str(r.endTime)=="13:00:00":
                                smrcolor26="red"
                            if str(r.endTime)=="14:00:00":
                                smrcolor26="red"
                                smrcolor27="red"
                                smrcolor28="red"
                            if str(r.endTime)=="15:00:00":
                                smrcolor26="red"
                                smrcolor27="red"
                                smrcolor28="red"
                                smrcolor29="red"
                                smrcolor30="red"
                        elif str(r.startTime)=="12:30:00":
                            smrcolor2="red"
                            if str(r.endTime)=="13:30:00":
                                smrcolor27="red"
                            if str(r.endTime)=="14:30:00":
                                smrcolor27="red"
                                smrcolor28="red"
                                smrcolor29="red"
                            if str(r.endTime)=="15:30:00":
                                smrcolor31="red"
                                smrcolor27="red"
                                smrcolor28="red"
                                smrcolor29="red"
                                smrcolor30="red"
                        elif str(r.startTime)=="13:00:00":
                            smrcolor27="red"
                            if str(r.endTime)=="14:00:00":
                                smrcolor28="red"
                            if str(r.endTime)=="15:00:00":
                                smrcolor28="red"
                                smrcolor29="red"
                                smrcolor30="red"
                            if str(r.endTime)=="16:00:00":
                                smrcolor32="red"
                                smrcolor31="red"
                                smrcolor28="red"
                                smrcolor29="red"
                                smrcolor30="red"
                        elif str(r.startTime)=="13:30:00":
                            smrcolor28="red"
                            if str(r.endTime)=="14:30:00":
                                smrcolor29="red"
                            if str(r.endTime)=="15:30:00":
                                smrcolor29="red"
                                smrcolor30="red"
                                smrcolor31="red"
                            if str(r.endTime)=="16:30:00":
                                smrcolor29="red"
                                smrcolor30="red"
                                smrcolor31="red"
                                smrcolor32="red"
                                smrcolor33="red"
                        elif str(r.startTime)=="14:00:00":
                            smrcolor29="red"
                            if str(r.endTime)=="15:00:00":
                                smrcolor30="red"
                            if str(r.endTime)=="06:00:00":
                                smrcolor30="red"
                                smrcolor31="red"
                                smrcolor32="red"
                            if str(r.endTime)=="17:00:00":
                                smrcolor34="red"
                                smrcolor30="red"
                                smrcolor31="red"
                                smrcolor32="red"
                                smrcolor33="red"
                        elif str(r.startTime)=="14:30:00":
                            smrcolor30="red"
                            if str(r.endTime)=="15:30:00":
                                smrcolor31="red"
                            if str(r.endTime)=="16:30:00":
                                smrcolor33="red"
                                smrcolor31="red"
                                smrcolor32="red"
                            if str(r.endTime)=="17:30:00":
                                smrcolor34="red"
                                smrcolor35="red"
                                smrcolor31="red"
                                smrcolor32="red"
                                smrcolor33="red"
                        elif str(r.startTime)=="15:00:00":
                            smrcolor31="red"
                            if str(r.endTime)=="16:00:00":
                                smrcolor32="red"
                            if str(r.endTime)=="17:00:00":
                                smrcolor33="red"
                                smrcolor34="red"
                                smrcolor32="red"
                            if str(r.endTime)=="18:00:00":
                                smrcolor34="red"
                                smrcolor35="red"
                                smrcolor12="red"
                                smrcolor32="red"
                                smrcolor33="red"
                        elif str(r.startTime)=="15:30:00":
                            smrcolor32="red"
                            if str(r.endTime)=="16:30:00":
                                smrcolor33="red"
                            if str(r.endTime)=="17:30:00":
                                smrcolor33="red"
                                smrcolor34="red"
                                smrcolor35="red"
                            if str(r.endTime)=="18:30:00":
                                smrcolor34="red"
                                smrcolor35="red"
                                smrcolor36="red"
                                smrcolor37="red"
                                smrcolor33="red"
                        elif str(r.startTime)=="16:00:00":
                            smrcolor33="red"
                            if str(r.endTime)=="17:00:00":
                                smrcolor34="red"
                            if str(r.endTime)=="18:00:00":
                                smrcolor36="red"
                                smrcolor34="red"
                                smrcolor35="red"
                            if str(r.endTime)=="19:00:00":
                                smrcolor34="red"
                                smrcolor35="red"
                                smrcolor36="red"
                                smrcolor37="red"
                                smrcolor38="red"
                        elif str(r.startTime)=="16:30:00":
                            smrcolor34="red"
                            if str(r.endTime)=="17:30:00":
                                smrcolor35="red"
                            if str(r.endTime)=="18:30:00":
                                smrcolor36="red"
                                smrcolor37="red"
                                smrcolor35="red"
                            if str(r.endTime)=="19:30:00":
                                smrcolor39="red"
                                smrcolor35="red"
                                smrcolor36="red"
                                smrcolor37="red"
                                smrcolor38="red"
                        elif str(r.startTime)=="17:00:00":
                            smrcolor35="red"
                            if str(r.endTime)=="18:00:00":
                                smrcolor36="red"
                            if str(r.endTime)=="19:00:00":
                                smrcolor36="red"
                                smrcolor37="red"
                                smrcolor38="red"
                            if str(r.endTime)=="20:00:00":
                                smrcolor39="red"
                                smrcolor40="red"
                                smrcolor36="red"
                                smrcolor37="red"
                                smrcolor38="red"
                        elif str(r.startTime)=="17:30:00":
                            smrcolor36="red"
                            if str(r.endTime)=="18:30:00":
                                smrcolor37="red"
                            if str(r.endTime)=="19:30:00":
                                smrcolor39="red"
                                smrcolor37="red"
                                smrcolor38="red"
                            if str(r.endTime)=="20:30:00":
                                smrcolor39="red"
                                smrcolor40="red"
                                smrcolor41="red"
                                smrcolor37="red"
                                smrcolor38="red"
                        elif str(r.startTime)=="18:00:00":
                            smrcolor37="red"
                            if str(r.endTime)=="19:00:00":
                                smrcolor38="red"
                            if str(r.endTime)=="20:00:00":
                                smrcolor39="red"
                                smrcolor40="red"
                                smrcolor38="red"
                            if str(r.endTime)=="21:00:00":
                                smrcolor39="red"
                                smrcolor40="red"
                                smrcolor41="red"
                                smrcolor42="red"
                                smrcolor38="red"
                        elif str(r.startTime)=="18:30:00":
                            smrcolor38="red"
                            if str(r.endTime)=="19:30:00":
                                smrcolor39="red"
                            if str(r.endTime)=="20:30:00":
                                smrcolor39="red"
                                smrcolor40="red"
                                smrcolor41="red"
                            if str(r.endTime)=="21:30:00":
                                smrcolor39="red"
                                smrcolor40="red"
                                smrcolor41="red"
                                smrcolor42="red"
                                smrcolor43="red"
                        elif str(r.startTime)=="19:00:00":
                            smrcolor39="red"
                            if str(r.endTime)=="20:00:00":
                                smrcolor40="red"
                            if str(r.endTime)=="21:00:00":
                                smrcolor42="red"
                                smrcolor40="red"
                                smrcolor41="red"
                            if str(r.endTime)=="22:00:00":
                                smrcolor44="red"
                                smrcolor40="red"
                                smrcolor41="red"
                                smrcolor42="red"
                                smrcolor43="red"
                        elif str(r.startTime)=="19:30:00":
                            smrcolor40="red"
                            if str(r.endTime)=="20:30:00":
                                smrcolor41="red"
                            if str(r.endTime)=="21:30:00":
                                smrcolor42="red"
                                smrcolor43="red"
                                smrcolor41="red"
                            if str(r.endTime)=="22:30:00":
                                smrcolor44="red"
                                smrcolor45="red"
                                smrcolor41="red"
                                smrcolor42="red"
                                smrcolor43="red"
                        elif str(r.startTime)=="08:00:00":
                            smrcolor41="red"
                            if str(r.endTime)=="09:00:00":
                                smrcolor42="red"
                            if str(r.endTime)=="10:00:00":
                                smrcolor42="red"
                                smrcolor43="red"
                                smrcolor44="red"
                            if str(r.endTime)=="11:00:00":
                                smrcolor44="red"
                                smrcolor45="red"
                                smrcolor46="red"
                                smrcolor42="red"
                                smrcolor43="red"
                        elif str(r.startTime)=="08:30:00":
                            smrcolor42="red"
                            if str(r.endTime)=="09:30:00":
                                smrcolor43="red"
                            if str(r.endTime)=="10:30:00":
                                smrcolor45="red"
                                smrcolor43="red"
                                smrcolor44="red"
                            if str(r.endTime)=="11:30:00":
                                smrcolor44="red"
                                smrcolor45="red"
                                smrcolor46="red"
                                smrcolor47="red"
                                smrcolor43="red"
                        elif str(r.startTime)=="21:00:00":
                            smrcolor43="red"
                            if str(r.endTime)=="22:00:00":
                                smrcolor44="red"
                            if str(r.endTime)=="23:00:00":
                                smrcolor45="red"
                                smrcolor46="red"
                                smrcolor44="red"
                            if str(r.endTime)=="00:00:00":
                                smrcolor44="red"
                                smrcolor45="red"
                                smrcolor46="red"
                                smrcolor47="red"
                                smrcolor48="red"
                        elif str(r.startTime)=="21:30:00":
                            smrcolor44="red"
                            if str(r.endTime)=="22:30:00":
                                smrcolor45="red"
                            if str(r.endTime)=="23:30:00":
                                smrcolor45="red"
                                smrcolor46="red"
                                smrcolor47="red"
                            if str(r.endTime)=="00:00:00":
                                #smrcolor25="red"
                                smrcolor45="red"
                                smrcolor46="red"
                                smrcolor47="red"
                                smrcolor48="red"
                        elif str(r.startTime)=="22:00:00":
                            smrcolor45="red"
                            if str(r.endTime)=="23:00:00":
                                smrcolor46="red"
                            if str(r.endTime)=="00:00:00":
                                smrcolor48="red"
                                smrcolor46="red"
                                smrcolor47="red"
                            if str(r.endTime)=="1:00:00":
                                #smrcolor25="red"
                                #smrcolor26="red"
                                smrcolor46="red"
                                smrcolor47="red"
                                smrcolor48="red"
                        elif str(r.startTime)=="22:30:00":
                            smrcolor46="red"
                            if str(r.endTime)=="23:30:00":
                                smrcolor47="red"
                            if str(r.endTime)=="00:30:00":
                                smrcolor48="red"
                                #smrcolor25="red"
                                smrcolor47="red"
                            if str(r.endTime)=="01:30:00":
                                #smrcolor25="red"
                                #smrcolor26="red"
                                #smrcolor27="red"
                                smrcolor47="red"
                                smrcolor48="red"
                        elif str(r.startTime)=="23:00:00":
                            smrcolor47="red"
                            if str(r.endTime)=="00:00:00":
                                smrcolor48="red"
                            if str(r.endTime)=="01:00:00":
                                smrcolor48="red"
                                #smrcolor25="red"
                                #smrcolor26="red"
                            if str(r.endTime)=="02:00:00":
                                #smrcolor25="red"
                                #smrcolor26="red"
                                #smrcolor27="red"
                                #smrcolor28="red"
                                smrcolor48="red"
                        elif str(r.startTime)=="23:30:00":
                            smrcolor48="red"
                            #if str(r.endTime)=="00:30:00":
                                #smrcolor25="red"
                            #elif str(r.endTime)=="01:30:00":
                                #smrcolor27="red"
                                #smrcolor25="red"
                                #smrcolor26="red"
                            #elif str(r.endTime)=="02:30:00":
                                #smrcolor25="red"
                                #smrcolor26="red"
                                #smrcolor27="red"
                                #smrcolor28="red"
                                #smrcolor29="red"
                    elif r.typeOf=="Training Room":
                        if str(r.startTime)=="00:00:00":
                            trcolor1="red"
                            if str(r.endTime)=="01:00:00":
                                trcolor2="red"
                            if str(r.endTime)=="02:00:00":
                                trcolor2="red"
                                trcolor3="red"
                                trcolor4="red"
                            if str(r.endTime)=="03:00:00":
                                trcolor2="red"
                                trcolor3="red"
                                trcolor4="red"
                                trcolor5="red"
                                trcolor6="red"
                        elif str(r.startTime)=="00:30:00":
                            trcolor2="red"
                            if str(r.endTime)=="01:30:00":
                                trcolor3="red"
                            if str(r.endTime)=="2:30:00":
                                trcolor3="red"
                                trcolor4="red"
                                trcolor5="red"
                            if str(r.endTime)=="3:30:00":
                                trcolor7="red"
                                trcolor3="red"
                                trcolor4="red"
                                trcolor5="red"
                                trcolor6="red"
                        elif str(r.startTime)=="01:00:00":
                            trcolor3="red"
                            if str(r.endTime)=="02:00:00":
                                trcolor4="red"
                            if str(r.endTime)=="03:00:00":
                                trcolor4="red"
                                trcolor5="red"
                                trcolor6="red"
                            if str(r.endTime)=="04:00:00":
                                trcolor8="red"
                                trcolor7="red"
                                trcolor4="red"
                                trcolor5="red"
                                trcolor6="red"
                        elif str(r.startTime)=="01:30:00":
                            trcolor4="red"
                            if str(r.endTime)=="02:30:00":
                                trcolor5="red"
                            if str(r.endTime)=="03:30:00":
                                trcolor5="red"
                                trcolor6="red"
                                trcolor7="red"
                            if str(r.endTime)=="04:30:00":
                                trcolor5="red"
                                trcolor6="red"
                                trcolor7="red"
                                trcolor8="red"
                                trcolor9="red"
                        elif str(r.startTime)=="02:00:00":
                            trcolor5="red"
                            if str(r.endTime)=="03:00:00":
                                trcolor6="red"
                            if str(r.endTime)=="04:00:00":
                                trcolor6="red"
                                trcolor7="red"
                                trcolor8="red"
                            if str(r.endTime)=="05:00:00":
                                trcolor10="red"
                                trcolor6="red"
                                trcolor7="red"
                                trcolor8="red"
                                trcolor9="red"
                        elif str(r.startTime)=="02:30:00":
                            trcolor6="red"
                            if str(r.endTime)=="03:30:00":
                                trcolor7="red"
                            if str(r.endTime)=="04:30:00":
                                trcolor9="red"
                                trcolor7="red"
                                trcolor8="red"
                            if str(r.endTime)=="05:30:00":
                                trcolor10="red"
                                trcolor11="red"
                                trcolor7="red"
                                trcolor8="red"
                                trcolor9="red"
                        elif str(r.startTime)=="03:00:00":
                            trcolor7="red"
                            if str(r.endTime)=="04:00:00":
                                trcolor8="red"
                            if str(r.endTime)=="05:00:00":
                                trcolor9="red"
                                trcolor10="red"
                                trcolor8="red"
                            if str(r.endTime)=="06:00:00":
                                trcolor10="red"
                                trcolor11="red"
                                trcolor12="red"
                                trcolor8="red"
                                trcolor9="red"
                        elif str(r.startTime)=="03:30:00":
                            trcolor8="red"
                            if str(r.endTime)=="04:30:00":
                                trcolor9="red"
                            if str(r.endTime)=="05:30:00":
                                trcolor9="red"
                                trcolor10="red"
                                trcolor11="red"
                            if str(r.endTime)=="06:30:00":
                                trcolor10="red"
                                trcolor11="red"
                                trcolor12="red"
                                trcolor13="red"
                                trcolor9="red"
                        elif str(r.startTime)=="04:00:00":
                            trcolor9="red"
                            if str(r.endTime)=="05:00:00":
                                trcolor10="red"
                            if str(r.endTime)=="06:00:00":
                                trcolor12="red"
                                trcolor10="red"
                                trcolor11="red"
                            if str(r.endTime)=="07:00:00":
                                trcolor10="red"
                                trcolor11="red"
                                trcolor12="red"
                                trcolor13="red"
                                trcolor14="red"
                        elif str(r.startTime)=="04:30:00":
                            trcolor10="red"
                            if str(r.endTime)=="05:30:00":
                                trcolor11="red"
                            if str(r.endTime)=="06:30:00":
                                trcolor12="red"
                                trcolor13="red"
                                trcolor11="red"
                            if str(r.endTime)=="07:30:00":
                                trcolor15="red"
                                trcolor11="red"
                                trcolor12="red"
                                trcolor13="red"
                                trcolor14="red"
                        elif str(r.startTime)=="05:00:00":
                            trcolor11="red"
                            if str(r.endTime)=="06:00:00":
                                trcolor12="red"
                            if str(r.endTime)=="07:00:00":
                                trcolor12="red"
                                trcolor13="red"
                                trcolor14="red"
                            if str(r.endTime)=="08:00:00":
                                trcolor15="red"
                                trcolor16="red"
                                trcolor12="red"
                                trcolor13="red"
                                trcolor14="red"
                        elif str(r.startTime)=="05:30:00":
                            trcolor12="red"
                            if str(r.endTime)=="06:30:00":
                                trcolor13="red"
                            if str(r.endTime)=="07:30:00":
                                trcolor15="red"
                                trcolor13="red"
                                trcolor14="red"
                            if str(r.endTime)=="08:30:00":
                                trcolor15="red"
                                trcolor16="red"
                                trcolor17="red"
                                trcolor13="red"
                                trcolor14="red"
                        elif str(r.startTime)=="06:00:00":
                            trcolor13="red"
                            if str(r.endTime)=="07:00:00":
                                trcolor14="red"
                            if str(r.endTime)=="08:00:00":
                                trcolor15="red"
                                trcolor16="red"
                                trcolor14="red"
                            if str(r.endTime)=="09:00:00":
                                trcolor15="red"
                                trcolor16="red"
                                trcolor17="red"
                                trcolor18="red"
                                trcolor14="red"
                        elif str(r.startTime)=="06:30:00":
                            trcolor14="red"
                            if str(r.endTime)=="07:30:00":
                                trcolor15="red"
                            if str(r.endTime)=="08:30:00":
                                trcolor15="red"
                                trcolor16="red"
                                trcolor17="red"
                            if str(r.endTime)=="09:30:00":
                                trcolor15="red"
                                trcolor16="red"
                                trcolor17="red"
                                trcolor18="red"
                                trcolor19="red"
                        elif str(r.startTime)=="07:00:00":
                            trcolor15="red"
                            if str(r.endTime)=="08:00:00":
                                trcolor16="red"
                            if str(r.endTime)=="09:00:00":
                                trcolor18="red"
                                trcolor16="red"
                                trcolor17="red"
                            if str(r.endTime)=="10:00:00":
                                trcolor20="red"
                                trcolor16="red"
                                trcolor17="red"
                                trcolor18="red"
                                trcolor19="red"
                        elif str(r.startTime)=="07:30:00":
                            trcolor16="red"
                            if str(r.endTime)=="08:30:00":
                                trcolor17="red"
                            if str(r.endTime)=="09:30:00":
                                trcolor18="red"
                                trcolor19="red"
                                trcolor17="red"
                            if str(r.endTime)=="10:30:00":
                                trcolor20="red"
                                trcolor21="red"
                                trcolor17="red"
                                trcolor18="red"
                                trcolor19="red"
                        elif str(r.startTime)=="08:00:00":
                            trcolor17="red"
                            if str(r.endTime)=="09:00:00":
                                trcolor18="red"
                            if str(r.endTime)=="10:00:00":
                                trcolor18="red"
                                trcolor19="red"
                                trcolor20="red"
                            if str(r.endTime)=="11:00:00":
                                trcolor20="red"
                                trcolor21="red"
                                trcolor22="red"
                                trcolor18="red"
                                trcolor19="red"
                        elif str(r.startTime)=="08:30:00":
                            trcolor18="red"
                            if str(r.endTime)=="09:30:00":
                                trcolor19="red"
                            if str(r.endTime)=="10:30:00":
                                trcolor21="red"
                                trcolor19="red"
                                trcolor20="red"
                            if str(r.endTime)=="11:30:00":
                                trcolor20="red"
                                trcolor21="red"
                                trcolor22="red"
                                trcolor23="red"
                                trcolor19="red"
                        elif str(r.startTime)=="09:00:00":
                            trcolor19="red"
                            if str(r.endTime)=="10:00:00":
                                trcolor20="red"
                            if str(r.endTime)=="11:00:00":
                                trcolor21="red"
                                trcolor22="red"
                                trcolor20="red"
                            if str(r.endTime)=="12:00:00":
                                trcolor20="red"
                                trcolor21="red"
                                trcolor22="red"
                                trcolor23="red"
                                trcolor24="red"
                        elif str(r.startTime)=="09:30:00":
                            trcolor20="red"
                            if str(r.endTime)=="10:30:00":
                                trcolor21="red"
                            if str(r.endTime)=="11:30:00":
                                trcolor21="red"
                                trcolor22="red"
                                trcolor23="red"
                            if str(r.endTime)=="12:30:00":
                                trcolor25="red"
                                trcolor21="red"
                                trcolor22="red"
                                trcolor23="red"
                                trcolor24="red"
                        elif str(r.startTime)=="10:00:00":
                            trcolor21="red"
                            if str(r.endTime)=="11:00:00":
                                trcolor22="red"
                            if str(r.endTime)=="12:00:00":
                                trcolor24="red"
                                trcolor22="red"
                                trcolor23="red"
                            if str(r.endTime)=="13:00:00":
                                trcolor25="red"
                                trcolor26="red"
                                trcolor22="red"
                                trcolor23="red"
                                trcolor24="red"
                        elif str(r.startTime)=="10:30:00":
                            trcolor22="red"
                            if str(r.endTime)=="11:00:00":
                                trcolor23="red"
                            if str(r.endTime)=="12:00:00":
                                trcolor24="red"
                                trcolor25="red"
                                trcolor23="red"
                            if str(r.endTime)=="13:00:00":
                                trcolor25="red"
                                trcolor26="red"
                                trcolor27="red"
                                trcolor23="red"
                                trcolor24="red"
                        elif str(r.startTime)=="11:00:00":
                            trcolor23="red"
                            if str(r.endTime)=="11:00:00":
                                trcolor24="red"
                            if str(r.endTime)=="12:00:00":
                                trcolor24="red"
                                trcolor25="red"
                                trcolor26="red"
                            if str(r.endTime)=="13:00:00":
                                trcolor25="red"
                                trcolor26="red"
                                trcolor27="red"
                                trcolor28="red"
                                trcolor24="red"
                        elif str(r.startTime)=="11:30:00":
                            trcolor24="red"
                            if str(r.endTime)=="12:30:00":
                                trcolor25="red"
                            if str(r.endTime)=="13:30:00":
                                trcolor27="red"
                                trcolor25="red"
                                trcolor26="red"
                            if str(r.endTime)=="14:30:00":
                                trcolor25="red"
                                trcolor26="red"
                                trcolor27="red"
                                trcolor28="red"
                                trcolor29="red"




                        elif str(r.startTime)=="12:00:00":
                            trcolor25="red"
                            if str(r.endTime)=="13:00:00":
                                trcolor26="red"
                            if str(r.endTime)=="14:00:00":
                                trcolor26="red"
                                trcolor27="red"
                                trcolor28="red"
                            if str(r.endTime)=="15:00:00":
                                trcolor26="red"
                                trcolor27="red"
                                trcolor28="red"
                                trcolor29="red"
                                trcolor30="red"
                        elif str(r.startTime)=="12:30:00":
                            trcolor2="red"
                            if str(r.endTime)=="13:30:00":
                                trcolor27="red"
                            if str(r.endTime)=="14:30:00":
                                trcolor27="red"
                                trcolor28="red"
                                trcolor29="red"
                            if str(r.endTime)=="15:30:00":
                                trcolor31="red"
                                trcolor27="red"
                                trcolor28="red"
                                trcolor29="red"
                                trcolor30="red"
                        elif str(r.startTime)=="13:00:00":
                            trcolor27="red"
                            if str(r.endTime)=="14:00:00":
                                trcolor28="red"
                            if str(r.endTime)=="15:00:00":
                                trcolor28="red"
                                trcolor29="red"
                                trcolor30="red"
                            if str(r.endTime)=="16:00:00":
                                trcolor32="red"
                                trcolor31="red"
                                trcolor28="red"
                                trcolor29="red"
                                trcolor30="red"
                        elif str(r.startTime)=="13:30:00":
                            trcolor28="red"
                            if str(r.endTime)=="14:30:00":
                                trcolor29="red"
                            if str(r.endTime)=="15:30:00":
                                trcolor29="red"
                                trcolor30="red"
                                trcolor31="red"
                            if str(r.endTime)=="16:30:00":
                                trcolor29="red"
                                trcolor30="red"
                                trcolor31="red"
                                trcolor32="red"
                                trcolor33="red"
                        elif str(r.startTime)=="14:00:00":
                            trcolor29="red"
                            if str(r.endTime)=="15:00:00":
                                trcolor30="red"
                            if str(r.endTime)=="06:00:00":
                                trcolor30="red"
                                trcolor31="red"
                                trcolor32="red"
                            if str(r.endTime)=="17:00:00":
                                trcolor34="red"
                                trcolor30="red"
                                trcolor31="red"
                                trcolor32="red"
                                trcolor33="red"
                        elif str(r.startTime)=="14:30:00":
                            trcolor30="red"
                            if str(r.endTime)=="15:30:00":
                                trcolor31="red"
                            if str(r.endTime)=="16:30:00":
                                trcolor33="red"
                                trcolor31="red"
                                trcolor32="red"
                            if str(r.endTime)=="17:30:00":
                                trcolor34="red"
                                trcolor35="red"
                                trcolor31="red"
                                trcolor32="red"
                                trcolor33="red"
                        elif str(r.startTime)=="15:00:00":
                            trcolor31="red"
                            if str(r.endTime)=="16:00:00":
                                trcolor32="red"
                            if str(r.endTime)=="17:00:00":
                                trcolor33="red"
                                trcolor34="red"
                                trcolor32="red"
                            if str(r.endTime)=="18:00:00":
                                trcolor34="red"
                                trcolor35="red"
                                trcolor12="red"
                                trcolor32="red"
                                trcolor33="red"
                        elif str(r.startTime)=="15:30:00":
                            trcolor32="red"
                            if str(r.endTime)=="16:30:00":
                                trcolor33="red"
                            if str(r.endTime)=="17:30:00":
                                trcolor33="red"
                                trcolor34="red"
                                trcolor35="red"
                            if str(r.endTime)=="18:30:00":
                                trcolor34="red"
                                trcolor35="red"
                                trcolor36="red"
                                trcolor37="red"
                                trcolor33="red"
                        elif str(r.startTime)=="16:00:00":
                            trcolor33="red"
                            if str(r.endTime)=="17:00:00":
                                trcolor34="red"
                            if str(r.endTime)=="18:00:00":
                                trcolor36="red"
                                trcolor34="red"
                                trcolor35="red"
                            if str(r.endTime)=="19:00:00":
                                trcolor34="red"
                                trcolor35="red"
                                trcolor36="red"
                                trcolor37="red"
                                trcolor38="red"
                        elif str(r.startTime)=="16:30:00":
                            trcolor34="red"
                            if str(r.endTime)=="17:30:00":
                                trcolor35="red"
                            if str(r.endTime)=="18:30:00":
                                trcolor36="red"
                                trcolor37="red"
                                trcolor35="red"
                            if str(r.endTime)=="19:30:00":
                                trcolor39="red"
                                trcolor35="red"
                                trcolor36="red"
                                trcolor37="red"
                                trcolor38="red"
                        elif str(r.startTime)=="17:00:00":
                            trcolor35="red"
                            if str(r.endTime)=="18:00:00":
                                trcolor36="red"
                            if str(r.endTime)=="19:00:00":
                                trcolor36="red"
                                trcolor37="red"
                                trcolor38="red"
                            if str(r.endTime)=="20:00:00":
                                trcolor39="red"
                                trcolor40="red"
                                trcolor36="red"
                                trcolor37="red"
                                trcolor38="red"
                        elif str(r.startTime)=="17:30:00":
                            trcolor36="red"
                            if str(r.endTime)=="18:30:00":
                                trcolor37="red"
                            if str(r.endTime)=="19:30:00":
                                trcolor39="red"
                                trcolor37="red"
                                trcolor38="red"
                            if str(r.endTime)=="20:30:00":
                                trcolor39="red"
                                trcolor40="red"
                                trcolor41="red"
                                trcolor37="red"
                                trcolor38="red"
                        elif str(r.startTime)=="18:00:00":
                            trcolor37="red"
                            if str(r.endTime)=="19:00:00":
                                trcolor38="red"
                            if str(r.endTime)=="20:00:00":
                                trcolor39="red"
                                trcolor40="red"
                                trcolor38="red"
                            if str(r.endTime)=="21:00:00":
                                trcolor39="red"
                                trcolor40="red"
                                trcolor41="red"
                                trcolor42="red"
                                trcolor38="red"
                        elif str(r.startTime)=="18:30:00":
                            trcolor38="red"
                            if str(r.endTime)=="19:30:00":
                                trcolor39="red"
                            if str(r.endTime)=="20:30:00":
                                trcolor39="red"
                                trcolor40="red"
                                trcolor41="red"
                            if str(r.endTime)=="21:30:00":
                                trcolor39="red"
                                trcolor40="red"
                                trcolor41="red"
                                trcolor42="red"
                                trcolor43="red"
                        elif str(r.startTime)=="19:00:00":
                            trcolor39="red"
                            if str(r.endTime)=="20:00:00":
                                trcolor40="red"
                            if str(r.endTime)=="21:00:00":
                                trcolor42="red"
                                trcolor40="red"
                                trcolor41="red"
                            if str(r.endTime)=="22:00:00":
                                trcolor44="red"
                                trcolor40="red"
                                trcolor41="red"
                                trcolor42="red"
                                trcolor43="red"
                        elif str(r.startTime)=="19:30:00":
                            trcolor40="red"
                            if str(r.endTime)=="20:30:00":
                                trcolor41="red"
                            if str(r.endTime)=="21:30:00":
                                trcolor42="red"
                                trcolor43="red"
                                trcolor41="red"
                            if str(r.endTime)=="22:30:00":
                                trcolor44="red"
                                trcolor45="red"
                                trcolor41="red"
                                trcolor42="red"
                                trcolor43="red"
                        elif str(r.startTime)=="08:00:00":
                            trcolor41="red"
                            if str(r.endTime)=="09:00:00":
                                trcolor42="red"
                            if str(r.endTime)=="10:00:00":
                                trcolor42="red"
                                trcolor43="red"
                                trcolor44="red"
                            if str(r.endTime)=="11:00:00":
                                trcolor44="red"
                                trcolor45="red"
                                trcolor46="red"
                                trcolor42="red"
                                trcolor43="red"
                        elif str(r.startTime)=="08:30:00":
                            trcolor42="red"
                            if str(r.endTime)=="09:30:00":
                                trcolor43="red"
                            if str(r.endTime)=="10:30:00":
                                trcolor45="red"
                                trcolor43="red"
                                trcolor44="red"
                            if str(r.endTime)=="11:30:00":
                                trcolor44="red"
                                trcolor45="red"
                                trcolor46="red"
                                trcolor47="red"
                                trcolor43="red"
                        elif str(r.startTime)=="21:00:00":
                            trcolor43="red"
                            if str(r.endTime)=="22:00:00":
                                trcolor44="red"
                            if str(r.endTime)=="23:00:00":
                                trcolor45="red"
                                trcolor46="red"
                                trcolor44="red"
                            if str(r.endTime)=="00:00:00":
                                trcolor44="red"
                                trcolor45="red"
                                trcolor46="red"
                                trcolor47="red"
                                trcolor48="red"
                        elif str(r.startTime)=="21:30:00":
                            trcolor44="red"
                            if str(r.endTime)=="22:30:00":
                                trcolor45="red"
                            if str(r.endTime)=="23:30:00":
                                trcolor45="red"
                                trcolor46="red"
                                trcolor47="red"
                            if str(r.endTime)=="00:00:00":
                                #trcolor25="red"
                                trcolor45="red"
                                trcolor46="red"
                                trcolor47="red"
                                trcolor48="red"
                        elif str(r.startTime)=="22:00:00":
                            trcolor45="red"
                            if str(r.endTime)=="23:00:00":
                                trcolor46="red"
                            if str(r.endTime)=="00:00:00":
                                trcolor48="red"
                                trcolor46="red"
                                trcolor47="red"
                            if str(r.endTime)=="1:00:00":
                                #trcolor25="red"
                                #trcolor26="red"
                                trcolor46="red"
                                trcolor47="red"
                                trcolor48="red"
                        elif str(r.startTime)=="22:30:00":
                            trcolor46="red"
                            if str(r.endTime)=="23:30:00":
                                trcolor47="red"
                            if str(r.endTime)=="00:30:00":
                                trcolor48="red"
                                #trcolor25="red"
                                trcolor47="red"
                            if str(r.endTime)=="01:30:00":
                                #trcolor25="red"
                                #trcolor26="red"
                                #trcolor27="red"
                                trcolor47="red"
                                trcolor48="red"
                        elif str(r.startTime)=="23:00:00":
                            trcolor47="red"
                            if str(r.endTime)=="00:00:00":
                                trcolor48="red"
                            if str(r.endTime)=="01:00:00":
                                trcolor48="red"
                                #trcolor25="red"
                                #trcolor26="red"
                            if str(r.endTime)=="02:00:00":
                                #trcolor25="red"
                                #trcolor26="red"
                                #trcolor27="red"
                                #trcolor28="red"
                                trcolor48="red"
                        elif str(r.startTime)=="23:30:00":
                            trcolor48="red"
                            #if str(r.endTime)=="00:30:00":
                                #trcolor25="red"
                            #elif str(r.endTime)=="01:30:00":
                                #trcolor27="red"
                                #trcolor25="red"
                                #trcolor26="red"
                            #elif str(r.endTime)=="02:30:00":
                                #trcolor25="red"
                                #trcolor26="red"
                                #trcolor27="red"
                                #trcolor28="red"
                                #trcolor29="red"
                    elif r.typeOf=="Big meeting room":
                        if str(r.startTime)=="00:00:00":
                            bmrcolor1="red"
                            if str(r.endTime)=="01:00:00":
                                bmrcolor2="red"
                            if str(r.endTime)=="02:00:00":
                                bmrcolor2="red"
                                bmrcolor3="red"
                                bmrcolor4="red"
                            if str(r.endTime)=="03:00:00":
                                bmrcolor2="red"
                                bmrcolor3="red"
                                bmrcolor4="red"
                                bmrcolor5="red"
                                bmrcolor6="red"
                        elif str(r.startTime)=="00:30:00":
                            bmrcolor2="red"
                            if str(r.endTime)=="01:30:00":
                                bmrcolor3="red"
                            if str(r.endTime)=="2:30:00":
                                bmrcolor3="red"
                                bmrcolor4="red"
                                bmrcolor5="red"
                            if str(r.endTime)=="3:30:00":
                                bmrcolor7="red"
                                bmrcolor3="red"
                                bmrcolor4="red"
                                bmrcolor5="red"
                                bmrcolor6="red"
                        elif str(r.startTime)=="01:00:00":
                            bmrcolor3="red"
                            if str(r.endTime)=="02:00:00":
                                bmrcolor4="red"
                            if str(r.endTime)=="03:00:00":
                                bmrcolor4="red"
                                bmrcolor5="red"
                                bmrcolor6="red"
                            if str(r.endTime)=="04:00:00":
                                bmrcolor8="red"
                                bmrcolor7="red"
                                bmrcolor4="red"
                                bmrcolor5="red"
                                bmrcolor6="red"
                        elif str(r.startTime)=="01:30:00":
                            bmrcolor4="red"
                            if str(r.endTime)=="02:30:00":
                                bmrcolor5="red"
                            if str(r.endTime)=="03:30:00":
                                bmrcolor5="red"
                                bmrcolor6="red"
                                bmrcolor7="red"
                            if str(r.endTime)=="04:30:00":
                                bmrcolor5="red"
                                bmrcolor6="red"
                                bmrcolor7="red"
                                bmrcolor8="red"
                                bmrcolor9="red"
                        elif str(r.startTime)=="02:00:00":
                            bmrcolor5="red"
                            if str(r.endTime)=="03:00:00":
                                bmrcolor6="red"
                            if str(r.endTime)=="04:00:00":
                                bmrcolor6="red"
                                bmrcolor7="red"
                                bmrcolor8="red"
                            if str(r.endTime)=="05:00:00":
                                bmrcolor10="red"
                                bmrcolor6="red"
                                bmrcolor7="red"
                                bmrcolor8="red"
                                bmrcolor9="red"
                        elif str(r.startTime)=="02:30:00":
                            bmrcolor6="red"
                            if str(r.endTime)=="03:30:00":
                                bmrcolor7="red"
                            if str(r.endTime)=="04:30:00":
                                bmrcolor9="red"
                                bmrcolor7="red"
                                bmrcolor8="red"
                            if str(r.endTime)=="05:30:00":
                                bmrcolor10="red"
                                bmrcolor11="red"
                                bmrcolor7="red"
                                bmrcolor8="red"
                                bmrcolor9="red"
                        elif str(r.startTime)=="03:00:00":
                            bmrcolor7="red"
                            if str(r.endTime)=="04:00:00":
                                bmrcolor8="red"
                            if str(r.endTime)=="05:00:00":
                                bmrcolor9="red"
                                bmrcolor10="red"
                                bmrcolor8="red"
                            if str(r.endTime)=="06:00:00":
                                bmrcolor10="red"
                                bmrcolor11="red"
                                bmrcolor12="red"
                                bmrcolor8="red"
                                bmrcolor9="red"
                        elif str(r.startTime)=="03:30:00":
                            bmrcolor8="red"
                            if str(r.endTime)=="04:30:00":
                                bmrcolor9="red"
                            if str(r.endTime)=="05:30:00":
                                bmrcolor9="red"
                                bmrcolor10="red"
                                bmrcolor11="red"
                            if str(r.endTime)=="06:30:00":
                                bmrcolor10="red"
                                bmrcolor11="red"
                                bmrcolor12="red"
                                bmrcolor13="red"
                                bmrcolor9="red"
                        elif str(r.startTime)=="04:00:00":
                            bmrcolor9="red"
                            if str(r.endTime)=="05:00:00":
                                bmrcolor10="red"
                            if str(r.endTime)=="06:00:00":
                                bmrcolor12="red"
                                bmrcolor10="red"
                                bmrcolor11="red"
                            if str(r.endTime)=="07:00:00":
                                bmrcolor10="red"
                                bmrcolor11="red"
                                bmrcolor12="red"
                                bmrcolor13="red"
                                bmrcolor14="red"
                        elif str(r.startTime)=="04:30:00":
                            bmrcolor10="red"
                            if str(r.endTime)=="05:30:00":
                                bmrcolor11="red"
                            if str(r.endTime)=="06:30:00":
                                bmrcolor12="red"
                                bmrcolor13="red"
                                bmrcolor11="red"
                            if str(r.endTime)=="07:30:00":
                                bmrcolor15="red"
                                bmrcolor11="red"
                                bmrcolor12="red"
                                bmrcolor13="red"
                                bmrcolor14="red"
                        elif str(r.startTime)=="05:00:00":
                            bmrcolor11="red"
                            if str(r.endTime)=="06:00:00":
                                bmrcolor12="red"
                            if str(r.endTime)=="07:00:00":
                                bmrcolor12="red"
                                bmrcolor13="red"
                                bmrcolor14="red"
                            if str(r.endTime)=="08:00:00":
                                bmrcolor15="red"
                                bmrcolor16="red"
                                bmrcolor12="red"
                                bmrcolor13="red"
                                bmrcolor14="red"
                        elif str(r.startTime)=="05:30:00":
                            bmrcolor12="red"
                            if str(r.endTime)=="06:30:00":
                                bmrcolor13="red"
                            if str(r.endTime)=="07:30:00":
                                bmrcolor15="red"
                                bmrcolor13="red"
                                bmrcolor14="red"
                            if str(r.endTime)=="08:30:00":
                                bmrcolor15="red"
                                bmrcolor16="red"
                                bmrcolor17="red"
                                bmrcolor13="red"
                                bmrcolor14="red"
                        elif str(r.startTime)=="06:00:00":
                            bmrcolor13="red"
                            if str(r.endTime)=="07:00:00":
                                bmrcolor14="red"
                            if str(r.endTime)=="08:00:00":
                                bmrcolor15="red"
                                bmrcolor16="red"
                                bmrcolor14="red"
                            if str(r.endTime)=="09:00:00":
                                bmrcolor15="red"
                                bmrcolor16="red"
                                bmrcolor17="red"
                                bmrcolor18="red"
                                bmrcolor14="red"
                        elif str(r.startTime)=="06:30:00":
                            bmrcolor14="red"
                            if str(r.endTime)=="07:30:00":
                                bmrcolor15="red"
                            if str(r.endTime)=="08:30:00":
                                bmrcolor15="red"
                                bmrcolor16="red"
                                bmrcolor17="red"
                            if str(r.endTime)=="09:30:00":
                                bmrcolor15="red"
                                bmrcolor16="red"
                                bmrcolor17="red"
                                bmrcolor18="red"
                                bmrcolor19="red"
                        elif str(r.startTime)=="07:00:00":
                            bmrcolor15="red"
                            if str(r.endTime)=="08:00:00":
                                bmrcolor16="red"
                            if str(r.endTime)=="09:00:00":
                                bmrcolor18="red"
                                bmrcolor16="red"
                                bmrcolor17="red"
                            if str(r.endTime)=="10:00:00":
                                bmrcolor20="red"
                                bmrcolor16="red"
                                bmrcolor17="red"
                                bmrcolor18="red"
                                bmrcolor19="red"
                        elif str(r.startTime)=="07:30:00":
                            bmrcolor16="red"
                            if str(r.endTime)=="08:30:00":
                                bmrcolor17="red"
                            if str(r.endTime)=="09:30:00":
                                bmrcolor18="red"
                                bmrcolor19="red"
                                bmrcolor17="red"
                            if str(r.endTime)=="10:30:00":
                                bmrcolor20="red"
                                bmrcolor21="red"
                                bmrcolor17="red"
                                bmrcolor18="red"
                                bmrcolor19="red"
                        elif str(r.startTime)=="08:00:00":
                            bmrcolor17="red"
                            if str(r.endTime)=="09:00:00":
                                bmrcolor18="red"
                            if str(r.endTime)=="10:00:00":
                                bmrcolor18="red"
                                bmrcolor19="red"
                                bmrcolor20="red"
                            if str(r.endTime)=="11:00:00":
                                bmrcolor20="red"
                                bmrcolor21="red"
                                bmrcolor22="red"
                                bmrcolor18="red"
                                bmrcolor19="red"
                        elif str(r.startTime)=="08:30:00":
                            bmrcolor18="red"
                            if str(r.endTime)=="09:30:00":
                                bmrcolor19="red"
                            if str(r.endTime)=="10:30:00":
                                bmrcolor21="red"
                                bmrcolor19="red"
                                bmrcolor20="red"
                            if str(r.endTime)=="11:30:00":
                                bmrcolor20="red"
                                bmrcolor21="red"
                                bmrcolor22="red"
                                bmrcolor23="red"
                                bmrcolor19="red"
                        elif str(r.startTime)=="09:00:00":
                            bmrcolor19="red"
                            if str(r.endTime)=="10:00:00":
                                bmrcolor20="red"
                            if str(r.endTime)=="11:00:00":
                                bmrcolor21="red"
                                bmrcolor22="red"
                                bmrcolor20="red"
                            if str(r.endTime)=="12:00:00":
                                bmrcolor20="red"
                                bmrcolor21="red"
                                bmrcolor22="red"
                                bmrcolor23="red"
                                bmrcolor24="red"
                        elif str(r.startTime)=="09:30:00":
                            bmrcolor20="red"
                            if str(r.endTime)=="10:30:00":
                                bmrcolor21="red"
                            if str(r.endTime)=="11:30:00":
                                bmrcolor21="red"
                                bmrcolor22="red"
                                bmrcolor23="red"
                            if str(r.endTime)=="12:30:00":
                                bmrcolor25="red"
                                bmrcolor21="red"
                                bmrcolor22="red"
                                bmrcolor23="red"
                                bmrcolor24="red"
                        elif str(r.startTime)=="10:00:00":
                            bmrcolor21="red"
                            if str(r.endTime)=="11:00:00":
                                bmrcolor22="red"
                            if str(r.endTime)=="12:00:00":
                                bmrcolor24="red"
                                bmrcolor22="red"
                                bmrcolor23="red"
                            if str(r.endTime)=="13:00:00":
                                bmrcolor25="red"
                                bmrcolor26="red"
                                bmrcolor22="red"
                                bmrcolor23="red"
                                bmrcolor24="red"
                        elif str(r.startTime)=="10:30:00":
                            bmrcolor22="red"
                            if str(r.endTime)=="11:00:00":
                                bmrcolor23="red"
                            if str(r.endTime)=="12:00:00":
                                bmrcolor24="red"
                                bmrcolor25="red"
                                bmrcolor23="red"
                            if str(r.endTime)=="13:00:00":
                                bmrcolor25="red"
                                bmrcolor26="red"
                                bmrcolor27="red"
                                bmrcolor23="red"
                                bmrcolor24="red"
                        elif str(r.startTime)=="11:00:00":
                            bmrcolor23="red"
                            if str(r.endTime)=="11:00:00":
                                bmrcolor24="red"
                            if str(r.endTime)=="12:00:00":
                                bmrcolor24="red"
                                bmrcolor25="red"
                                bmrcolor26="red"
                            if str(r.endTime)=="13:00:00":
                                bmrcolor25="red"
                                bmrcolor26="red"
                                bmrcolor27="red"
                                bmrcolor28="red"
                                bmrcolor24="red"
                        elif str(r.startTime)=="11:30:00":
                            bmrcolor24="red"
                            if str(r.endTime)=="12:30:00":
                                bmrcolor25="red"
                            if str(r.endTime)=="13:30:00":
                                bmrcolor27="red"
                                bmrcolor25="red"
                                bmrcolor26="red"
                            if str(r.endTime)=="14:30:00":
                                bmrcolor25="red"
                                bmrcolor26="red"
                                bmrcolor27="red"
                                bmrcolor28="red"
                                bmrcolor29="red"




                        elif str(r.startTime)=="12:00:00":
                            bmrcolor25="red"
                            if str(r.endTime)=="13:00:00":
                                bmrcolor26="red"
                            if str(r.endTime)=="14:00:00":
                                bmrcolor26="red"
                                bmrcolor27="red"
                                bmrcolor28="red"
                            if str(r.endTime)=="15:00:00":
                                bmrcolor26="red"
                                bmrcolor27="red"
                                bmrcolor28="red"
                                bmrcolor29="red"
                                bmrcolor30="red"
                        elif str(r.startTime)=="12:30:00":
                            bmrcolor2="red"
                            if str(r.endTime)=="13:30:00":
                                bmrcolor27="red"
                            if str(r.endTime)=="14:30:00":
                                bmrcolor27="red"
                                bmrcolor28="red"
                                bmrcolor29="red"
                            if str(r.endTime)=="15:30:00":
                                bmrcolor31="red"
                                bmrcolor27="red"
                                bmrcolor28="red"
                                bmrcolor29="red"
                                bmrcolor30="red"
                        elif str(r.startTime)=="13:00:00":
                            bmrcolor27="red"
                            if str(r.endTime)=="14:00:00":
                                bmrcolor28="red"
                            if str(r.endTime)=="15:00:00":
                                bmrcolor28="red"
                                bmrcolor29="red"
                                bmrcolor30="red"
                            if str(r.endTime)=="16:00:00":
                                bmrcolor32="red"
                                bmrcolor31="red"
                                bmrcolor28="red"
                                bmrcolor29="red"
                                bmrcolor30="red"
                        elif str(r.startTime)=="13:30:00":
                            bmrcolor28="red"
                            if str(r.endTime)=="14:30:00":
                                bmrcolor29="red"
                            if str(r.endTime)=="15:30:00":
                                bmrcolor29="red"
                                bmrcolor30="red"
                                bmrcolor31="red"
                            if str(r.endTime)=="16:30:00":
                                bmrcolor29="red"
                                bmrcolor30="red"
                                bmrcolor31="red"
                                bmrcolor32="red"
                                bmrcolor33="red"
                        elif str(r.startTime)=="14:00:00":
                            bmrcolor29="red"
                            if str(r.endTime)=="15:00:00":
                                bmrcolor30="red"
                            if str(r.endTime)=="06:00:00":
                                bmrcolor30="red"
                                bmrcolor31="red"
                                bmrcolor32="red"
                            if str(r.endTime)=="17:00:00":
                                bmrcolor34="red"
                                bmrcolor30="red"
                                bmrcolor31="red"
                                bmrcolor32="red"
                                bmrcolor33="red"
                        elif str(r.startTime)=="14:30:00":
                            bmrcolor30="red"
                            if str(r.endTime)=="15:30:00":
                                bmrcolor31="red"
                            if str(r.endTime)=="16:30:00":
                                bmrcolor33="red"
                                bmrcolor31="red"
                                bmrcolor32="red"
                            if str(r.endTime)=="17:30:00":
                                bmrcolor34="red"
                                bmrcolor35="red"
                                bmrcolor31="red"
                                bmrcolor32="red"
                                bmrcolor33="red"
                        elif str(r.startTime)=="15:00:00":
                            bmrcolor31="red"
                            if str(r.endTime)=="16:00:00":
                                bmrcolor32="red"
                            if str(r.endTime)=="17:00:00":
                                bmrcolor33="red"
                                bmrcolor34="red"
                                bmrcolor32="red"
                            if str(r.endTime)=="18:00:00":
                                bmrcolor34="red"
                                bmrcolor35="red"
                                bmrcolor12="red"
                                bmrcolor32="red"
                                bmrcolor33="red"
                        elif str(r.startTime)=="15:30:00":
                            bmrcolor32="red"
                            if str(r.endTime)=="16:30:00":
                                bmrcolor33="red"
                            if str(r.endTime)=="17:30:00":
                                bmrcolor33="red"
                                bmrcolor34="red"
                                bmrcolor35="red"
                            if str(r.endTime)=="18:30:00":
                                bmrcolor34="red"
                                bmrcolor35="red"
                                bmrcolor36="red"
                                bmrcolor37="red"
                                bmrcolor33="red"
                        elif str(r.startTime)=="16:00:00":
                            bmrcolor33="red"
                            if str(r.endTime)=="17:00:00":
                                bmrcolor34="red"
                            if str(r.endTime)=="18:00:00":
                                bmrcolor36="red"
                                bmrcolor34="red"
                                bmrcolor35="red"
                            if str(r.endTime)=="19:00:00":
                                bmrcolor34="red"
                                bmrcolor35="red"
                                bmrcolor36="red"
                                bmrcolor37="red"
                                bmrcolor38="red"
                        elif str(r.startTime)=="16:30:00":
                            bmrcolor34="red"
                            if str(r.endTime)=="17:30:00":
                                bmrcolor35="red"
                            if str(r.endTime)=="18:30:00":
                                bmrcolor36="red"
                                bmrcolor37="red"
                                bmrcolor35="red"
                            if str(r.endTime)=="19:30:00":
                                bmrcolor39="red"
                                bmrcolor35="red"
                                bmrcolor36="red"
                                bmrcolor37="red"
                                bmrcolor38="red"
                        elif str(r.startTime)=="17:00:00":
                            bmrcolor35="red"
                            if str(r.endTime)=="18:00:00":
                                bmrcolor36="red"
                            if str(r.endTime)=="19:00:00":
                                bmrcolor36="red"
                                bmrcolor37="red"
                                bmrcolor38="red"
                            if str(r.endTime)=="20:00:00":
                                bmrcolor39="red"
                                bmrcolor40="red"
                                bmrcolor36="red"
                                bmrcolor37="red"
                                bmrcolor38="red"
                        elif str(r.startTime)=="17:30:00":
                            bmrcolor36="red"
                            if str(r.endTime)=="18:30:00":
                                bmrcolor37="red"
                            if str(r.endTime)=="19:30:00":
                                bmrcolor39="red"
                                bmrcolor37="red"
                                bmrcolor38="red"
                            if str(r.endTime)=="20:30:00":
                                bmrcolor39="red"
                                bmrcolor40="red"
                                bmrcolor41="red"
                                bmrcolor37="red"
                                bmrcolor38="red"
                        elif str(r.startTime)=="18:00:00":
                            bmrcolor37="red"
                            if str(r.endTime)=="19:00:00":
                                bmrcolor38="red"
                            if str(r.endTime)=="20:00:00":
                                bmrcolor39="red"
                                bmrcolor40="red"
                                bmrcolor38="red"
                            if str(r.endTime)=="21:00:00":
                                bmrcolor39="red"
                                bmrcolor40="red"
                                bmrcolor41="red"
                                bmrcolor42="red"
                                bmrcolor38="red"
                        elif str(r.startTime)=="18:30:00":
                            bmrcolor38="red"
                            if str(r.endTime)=="19:30:00":
                                bmrcolor39="red"
                            if str(r.endTime)=="20:30:00":
                                bmrcolor39="red"
                                bmrcolor40="red"
                                bmrcolor41="red"
                            if str(r.endTime)=="21:30:00":
                                bmrcolor39="red"
                                bmrcolor40="red"
                                bmrcolor41="red"
                                bmrcolor42="red"
                                bmrcolor43="red"
                        elif str(r.startTime)=="19:00:00":
                            bmrcolor39="red"
                            if str(r.endTime)=="20:00:00":
                                bmrcolor40="red"
                            if str(r.endTime)=="21:00:00":
                                bmrcolor42="red"
                                bmrcolor40="red"
                                bmrcolor41="red"
                            if str(r.endTime)=="22:00:00":
                                bmrcolor44="red"
                                bmrcolor40="red"
                                bmrcolor41="red"
                                bmrcolor42="red"
                                bmrcolor43="red"
                        elif str(r.startTime)=="19:30:00":
                            bmrcolor40="red"
                            if str(r.endTime)=="20:30:00":
                                bmrcolor41="red"
                            if str(r.endTime)=="21:30:00":
                                bmrcolor42="red"
                                bmrcolor43="red"
                                bmrcolor41="red"
                            if str(r.endTime)=="22:30:00":
                                bmrcolor44="red"
                                bmrcolor45="red"
                                bmrcolor41="red"
                                bmrcolor42="red"
                                bmrcolor43="red"
                        elif str(r.startTime)=="08:00:00":
                            bmrcolor41="red"
                            if str(r.endTime)=="09:00:00":
                                bmrcolor42="red"
                            if str(r.endTime)=="10:00:00":
                                bmrcolor42="red"
                                bmrcolor43="red"
                                bmrcolor44="red"
                            if str(r.endTime)=="11:00:00":
                                bmrcolor44="red"
                                bmrcolor45="red"
                                bmrcolor46="red"
                                bmrcolor42="red"
                                bmrcolor43="red"
                        elif str(r.startTime)=="08:30:00":
                            bmrcolor42="red"
                            if str(r.endTime)=="09:30:00":
                                bmrcolor43="red"
                            if str(r.endTime)=="10:30:00":
                                bmrcolor45="red"
                                bmrcolor43="red"
                                bmrcolor44="red"
                            if str(r.endTime)=="11:30:00":
                                bmrcolor44="red"
                                bmrcolor45="red"
                                bmrcolor46="red"
                                bmrcolor47="red"
                                bmrcolor43="red"
                        elif str(r.startTime)=="21:00:00":
                            bmrcolor43="red"
                            if str(r.endTime)=="22:00:00":
                                bmrcolor44="red"
                            if str(r.endTime)=="23:00:00":
                                bmrcolor45="red"
                                bmrcolor46="red"
                                bmrcolor44="red"
                            if str(r.endTime)=="00:00:00":
                                bmrcolor44="red"
                                bmrcolor45="red"
                                bmrcolor46="red"
                                bmrcolor47="red"
                                bmrcolor48="red"
                        elif str(r.startTime)=="21:30:00":
                            bmrcolor44="red"
                            if str(r.endTime)=="22:30:00":
                                bmrcolor45="red"
                            if str(r.endTime)=="23:30:00":
                                bmrcolor45="red"
                                bmrcolor46="red"
                                bmrcolor47="red"
                            if str(r.endTime)=="00:00:00":
                                #bmrcolor25="red"
                                bmrcolor45="red"
                                bmrcolor46="red"
                                bmrcolor47="red"
                                bmrcolor48="red"
                        elif str(r.startTime)=="22:00:00":
                            bmrcolor45="red"
                            if str(r.endTime)=="23:00:00":
                                bmrcolor46="red"
                            if str(r.endTime)=="00:00:00":
                                bmrcolor48="red"
                                bmrcolor46="red"
                                bmrcolor47="red"
                            if str(r.endTime)=="1:00:00":
                                #bmrcolor25="red"
                                #bmrcolor26="red"
                                bmrcolor46="red"
                                bmrcolor47="red"
                                bmrcolor48="red"
                        elif str(r.startTime)=="22:30:00":
                            bmrcolor46="red"
                            if str(r.endTime)=="23:30:00":
                                bmrcolor47="red"
                            if str(r.endTime)=="00:30:00":
                                bmrcolor48="red"
                                #bmrcolor25="red"
                                bmrcolor47="red"
                            if str(r.endTime)=="01:30:00":
                                #bmrcolor25="red"
                                #bmrcolor26="red"
                                #bmrcolor27="red"
                                bmrcolor47="red"
                                bmrcolor48="red"
                        elif str(r.startTime)=="23:00:00":
                            bmrcolor47="red"
                            if str(r.endTime)=="00:00:00":
                                bmrcolor48="red"
                            if str(r.endTime)=="01:00:00":
                                bmrcolor48="red"
                                #bmrcolor25="red"
                                #bmrcolor26="red"
                            if str(r.endTime)=="02:00:00":
                                #bmrcolor25="red"
                                #bmrcolor26="red"
                                #bmrcolor27="red"
                                #bmrcolor28="red"
                                bmrcolor48="red"
                        elif str(r.startTime)=="23:30:00":
                            bmrcolor48="red"
                            #if str(r.endTime)=="00:30:00":
                                #bmrcolor25="red"
                            #elif str(r.endTime)=="01:30:00":
                                #bmrcolor27="red"
                                #bmrcolor25="red"
                                #bmrcolor26="red"
                            #elif str(r.endTime)=="02:30:00":
                                #bmrcolor25="red"
                                #trcolor26="red"
                                #bmrcolor27="red"
                                #bmrcolor28="red"
                                #bmrcolor29="red"


    if request.method == "POST":
        reservationform= forms.reserve(request.POST)
        #Multi Access management
        for r in res_list :
            if r.typeOf == request.POST.get('typeOf') :

                if (str(r.date) == (datetime.datetime.strptime(request.POST.get('date'),'%m/%d/%Y').strftime('%Y-%m-%d'))):
                    if (datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time() == r.startTime):
                        message = "A meeting starts at this time ! Room reserved !"
                        return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,
                        'smrcolor1':smrcolor1,'smrcolor2':smrcolor2,'smrcolor3':smrcolor3,'smrcolor4':smrcolor4,'smrcolor5':smrcolor5,'smrcolor6':smrcolor6,'smrcolor7':smrcolor7,
                        'smrcolor8':smrcolor8,'smrcolor9':smrcolor9,'smrcolor10':smrcolor10,'smrcolor11':smrcolor11,'smrcolor12':smrcolor12,'smrcolor13':smrcolor13,
                        'smrcolor14':smrcolor14,'smrcolor15':smrcolor15,'smrcolor16':smrcolor16,'smrcolor17':smrcolor17,'smrcolor18':smrcolor18,'smrcolor19':smrcolor19,
                        'smrcolor20':smrcolor20,'smrcolor21':smrcolor21,'smrcolor22':smrcolor22,'smrcolor23':smrcolor23,'smrcolor24':smrcolor24,'smrcolor25':smrcolor25,
                        'smrcolor26':smrcolor26,'smrcolor27':smrcolor27,'smrcolor28':smrcolor28,'smrcolor29':smrcolor29,'smrcolor30':smrcolor30,'smrcolor31':smrcolor31,
                        'smrcolor32':smrcolor32,'smrcolor33':smrcolor33,'smrcolor34':smrcolor34,'smrcolor35':smrcolor35,'smrcolor36':smrcolor36,'smrcolor37':smrcolor37,
                        'smrcolor38':smrcolor38,'smrcolor39':smrcolor39,'smrcolor40':smrcolor40,'smrcolor41':smrcolor41,'smrcolor42':smrcolor42,'smrcolor43':smrcolor43,
                        'smrcolor44':smrcolor44,'smrcolor45':smrcolor45,'smrcolor46':smrcolor46,'smrcolor47':smrcolor47,'smrcolor48':smrcolor48,

                        'trcolor1':trcolor1,'trcolor2':trcolor2,'trcolor3':trcolor3,'trcolor4':trcolor4,'trcolor5':trcolor5,'trcolor6':trcolor6,'trcolor7':trcolor7,
                        'trcolor8':trcolor8,'trcolor9':trcolor9,'trcolor10':trcolor10,'trcolor11':trcolor11,'trcolor12':trcolor12,'trcolor13':trcolor13,
                        'trcolor14':trcolor14,'trcolor15':trcolor15,'trcolor16':trcolor16,'trcolor17':trcolor17,'trcolor18':trcolor18,'trcolor19':trcolor19,
                        'trcolor20':trcolor20,'trcolor21':trcolor21,'trcolor22':trcolor22,'trcolor23':trcolor23,'trcolor24':trcolor24,'trcolor25':trcolor25,
                        'trcolor26':trcolor26,'trcolor27':trcolor27,'trcolor28':trcolor28,'trcolor29':trcolor29,'trcolor30':trcolor30,'trcolor31':trcolor31,
                        'trcolor32':trcolor32,'trcolor33':trcolor33,'trcolor34':trcolor34,'trcolor35':trcolor35,'trcolor36':trcolor36,'trcolor37':trcolor37,
                        'trcolor38':trcolor38,'trcolor39':trcolor39,'trcolor40':trcolor40,'trcolor41':trcolor41,'trcolor42':trcolor42,'trcolor43':trcolor43,
                        'trcolor44':trcolor44,'trcolor45':trcolor45,'trcolor46':trcolor46,'trcolor47':trcolor47,'trcolor48':trcolor48,

                        'bmrcolor1':bmrcolor1,'bmrcolor2':bmrcolor2,'bmrcolor3':bmrcolor3,'bmrcolor4':bmrcolor4,'bmrcolor5':bmrcolor5,'bmrcolor6':bmrcolor6,'bmrcolor7':bmrcolor7,
                        'bmrcolor8':bmrcolor8,'bmrcolor9':bmrcolor9,'bmrcolor10':bmrcolor10,'bmrcolor11':bmrcolor11,'bmrcolor12':bmrcolor12,'bmrcolor13':bmrcolor13,
                        'bmrcolor14':bmrcolor14,'bmrcolor15':bmrcolor15,'bmrcolor16':bmrcolor16,'bmrcolor17':bmrcolor17,'bmrcolor18':bmrcolor18,'bmrcolor19':bmrcolor19,
                        'bmrcolor20':bmrcolor20,'bmrcolor21':bmrcolor21,'bmrcolor22':bmrcolor22,'bmrcolor23':bmrcolor23,'bmrcolor24':bmrcolor24,'bmrcolor25':bmrcolor25,
                        'bmrcolor26':bmrcolor26,'bmrcolor27':bmrcolor27,'bmrcolor28':bmrcolor28,'bmrcolor29':bmrcolor29,'bmrcolor30':bmrcolor30,'bmrcolor31':bmrcolor31,
                        'bmrcolor32':bmrcolor32,'bmrcolor33':bmrcolor33,'bmrcolor34':bmrcolor34,'bmrcolor35':bmrcolor35,'bmrcolor36':bmrcolor36,'bmrcolor37':bmrcolor37,
                        'bmrcolor38':bmrcolor38,'bmrcolor39':bmrcolor39,'bmrcolor40':bmrcolor40,'bmrcolor41':bmrcolor41,'bmrcolor42':bmrcolor42,'bmrcolor43':bmrcolor43,
                        'bmrcolor44':bmrcolor44,'bmrcolor45':bmrcolor45,'bmrcolor46':bmrcolor46,'bmrcolor47':bmrcolor47,'bmrcolor48':bmrcolor48,
                    })
                    else :
                        if int(request.POST.get('extraTime'))>0 :
                            end=((datetime.datetime.combine(datetime.date(12, 12, 10), r.startTime) + datetime.timedelta(minutes=int(r.duration))).time())
                            formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(hours=int(request.POST.get('extraTime')))).time())

                        else:
                            end=((datetime.datetime.combine(datetime.date(12, 12, 10), r.startTime) + datetime.timedelta(minutes=int(r.duration))).time())
                            formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(minutes=int(request.POST.get('duration')))).time())

                        if  (datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time() > r.startTime and datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()<end) :
                            message = "A meeting is taking place at this time !"
                            return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,
                            'smrcolor1':smrcolor1,'smrcolor2':smrcolor2,'smrcolor3':smrcolor3,'smrcolor4':smrcolor4,'smrcolor5':smrcolor5,'smrcolor6':smrcolor6,'smrcolor7':smrcolor7,
                            'smrcolor8':smrcolor8,'smrcolor9':smrcolor9,'smrcolor10':smrcolor10,'smrcolor11':smrcolor11,'smrcolor12':smrcolor12,'smrcolor13':smrcolor13,
                            'smrcolor14':smrcolor14,'smrcolor15':smrcolor15,'smrcolor16':smrcolor16,'smrcolor17':smrcolor17,'smrcolor18':smrcolor18,'smrcolor19':smrcolor19,
                            'smrcolor20':smrcolor20,'smrcolor21':smrcolor21,'smrcolor22':smrcolor22,'smrcolor23':smrcolor23,'smrcolor24':smrcolor24,'smrcolor25':smrcolor25,
                            'smrcolor26':smrcolor26,'smrcolor27':smrcolor27,'smrcolor28':smrcolor28,'smrcolor29':smrcolor29,'smrcolor30':smrcolor30,'smrcolor31':smrcolor31,
                            'smrcolor32':smrcolor32,'smrcolor33':smrcolor33,'smrcolor34':smrcolor34,'smrcolor35':smrcolor35,'smrcolor36':smrcolor36,'smrcolor37':smrcolor37,
                            'smrcolor38':smrcolor38,'smrcolor39':smrcolor39,'smrcolor40':smrcolor40,'smrcolor41':smrcolor41,'smrcolor42':smrcolor42,'smrcolor43':smrcolor43,
                            'smrcolor44':smrcolor44,'smrcolor45':smrcolor45,'smrcolor46':smrcolor46,'smrcolor47':smrcolor47,'smrcolor48':smrcolor48,

                            'trcolor1':trcolor1,'trcolor2':trcolor2,'trcolor3':trcolor3,'trcolor4':trcolor4,'trcolor5':trcolor5,'trcolor6':trcolor6,'trcolor7':trcolor7,
                            'trcolor8':trcolor8,'trcolor9':trcolor9,'trcolor10':trcolor10,'trcolor11':trcolor11,'trcolor12':trcolor12,'trcolor13':trcolor13,
                            'trcolor14':trcolor14,'trcolor15':trcolor15,'trcolor16':trcolor16,'trcolor17':trcolor17,'trcolor18':trcolor18,'trcolor19':trcolor19,
                            'trcolor20':trcolor20,'trcolor21':trcolor21,'trcolor22':trcolor22,'trcolor23':trcolor23,'trcolor24':trcolor24,'trcolor25':trcolor25,
                            'trcolor26':trcolor26,'trcolor27':trcolor27,'trcolor28':trcolor28,'trcolor29':trcolor29,'trcolor30':trcolor30,'trcolor31':trcolor31,
                            'trcolor32':trcolor32,'trcolor33':trcolor33,'trcolor34':trcolor34,'trcolor35':trcolor35,'trcolor36':trcolor36,'trcolor37':trcolor37,
                            'trcolor38':trcolor38,'trcolor39':trcolor39,'trcolor40':trcolor40,'trcolor41':trcolor41,'trcolor42':trcolor42,'trcolor43':trcolor43,
                            'trcolor44':trcolor44,'trcolor45':trcolor45,'trcolor46':trcolor46,'trcolor47':trcolor47,'trcolor48':trcolor48,

                            'bmrcolor1':bmrcolor1,'bmrcolor2':bmrcolor2,'bmrcolor3':bmrcolor3,'bmrcolor4':bmrcolor4,'bmrcolor5':bmrcolor5,'bmrcolor6':bmrcolor6,'bmrcolor7':bmrcolor7,
                            'bmrcolor8':bmrcolor8,'bmrcolor9':bmrcolor9,'bmrcolor10':bmrcolor10,'bmrcolor11':bmrcolor11,'bmrcolor12':bmrcolor12,'bmrcolor13':bmrcolor13,
                            'bmrcolor14':bmrcolor14,'bmrcolor15':bmrcolor15,'bmrcolor16':bmrcolor16,'bmrcolor17':bmrcolor17,'bmrcolor18':bmrcolor18,'bmrcolor19':bmrcolor19,
                            'bmrcolor20':bmrcolor20,'bmrcolor21':bmrcolor21,'bmrcolor22':bmrcolor22,'bmrcolor23':bmrcolor23,'bmrcolor24':bmrcolor24,'bmrcolor25':bmrcolor25,
                            'bmrcolor26':bmrcolor26,'bmrcolor27':bmrcolor27,'bmrcolor28':bmrcolor28,'bmrcolor29':bmrcolor29,'bmrcolor30':bmrcolor30,'bmrcolor31':bmrcolor31,
                            'bmrcolor32':bmrcolor32,'bmrcolor33':bmrcolor33,'bmrcolor34':bmrcolor34,'bmrcolor35':bmrcolor35,'bmrcolor36':bmrcolor36,'bmrcolor37':bmrcolor37,
                            'bmrcolor38':bmrcolor38,'bmrcolor39':bmrcolor39,'bmrcolor40':bmrcolor40,'bmrcolor41':bmrcolor41,'bmrcolor42':bmrcolor42,'bmrcolor43':bmrcolor43,
                            'bmrcolor44':bmrcolor44,'bmrcolor45':bmrcolor45,'bmrcolor46':bmrcolor46,'bmrcolor47':bmrcolor47,'bmrcolor48':bmrcolor48,
                        })
                        elif (formend>r.startTime and datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()<end):
                            message = "A meeting is taking place at this time !"
                            return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,
                            'smrcolor1':smrcolor1,'smrcolor2':smrcolor2,'smrcolor3':smrcolor3,'smrcolor4':smrcolor4,'smrcolor5':smrcolor5,'smrcolor6':smrcolor6,'smrcolor7':smrcolor7,
                            'smrcolor8':smrcolor8,'smrcolor9':smrcolor9,'smrcolor10':smrcolor10,'smrcolor11':smrcolor11,'smrcolor12':smrcolor12,'smrcolor13':smrcolor13,
                            'smrcolor14':smrcolor14,'smrcolor15':smrcolor15,'smrcolor16':smrcolor16,'smrcolor17':smrcolor17,'smrcolor18':smrcolor18,'smrcolor19':smrcolor19,
                            'smrcolor20':smrcolor20,'smrcolor21':smrcolor21,'smrcolor22':smrcolor22,'smrcolor23':smrcolor23,'smrcolor24':smrcolor24,'smrcolor25':smrcolor25,
                            'smrcolor26':smrcolor26,'smrcolor27':smrcolor27,'smrcolor28':smrcolor28,'smrcolor29':smrcolor29,'smrcolor30':smrcolor30,'smrcolor31':smrcolor31,
                            'smrcolor32':smrcolor32,'smrcolor33':smrcolor33,'smrcolor34':smrcolor34,'smrcolor35':smrcolor35,'smrcolor36':smrcolor36,'smrcolor37':smrcolor37,
                            'smrcolor38':smrcolor38,'smrcolor39':smrcolor39,'smrcolor40':smrcolor40,'smrcolor41':smrcolor41,'smrcolor42':smrcolor42,'smrcolor43':smrcolor43,
                            'smrcolor44':smrcolor44,'smrcolor45':smrcolor45,'smrcolor46':smrcolor46,'smrcolor47':smrcolor47,'smrcolor48':smrcolor48,

                            'trcolor1':trcolor1,'trcolor2':trcolor2,'trcolor3':trcolor3,'trcolor4':trcolor4,'trcolor5':trcolor5,'trcolor6':trcolor6,'trcolor7':trcolor7,
                            'trcolor8':trcolor8,'trcolor9':trcolor9,'trcolor10':trcolor10,'trcolor11':trcolor11,'trcolor12':trcolor12,'trcolor13':trcolor13,
                            'trcolor14':trcolor14,'trcolor15':trcolor15,'trcolor16':trcolor16,'trcolor17':trcolor17,'trcolor18':trcolor18,'trcolor19':trcolor19,
                            'trcolor20':trcolor20,'trcolor21':trcolor21,'trcolor22':trcolor22,'trcolor23':trcolor23,'trcolor24':trcolor24,'trcolor25':trcolor25,
                            'trcolor26':trcolor26,'trcolor27':trcolor27,'trcolor28':trcolor28,'trcolor29':trcolor29,'trcolor30':trcolor30,'trcolor31':trcolor31,
                            'trcolor32':trcolor32,'trcolor33':trcolor33,'trcolor34':trcolor34,'trcolor35':trcolor35,'trcolor36':trcolor36,'trcolor37':trcolor37,
                            'trcolor38':trcolor38,'trcolor39':trcolor39,'trcolor40':trcolor40,'trcolor41':trcolor41,'trcolor42':trcolor42,'trcolor43':trcolor43,
                            'trcolor44':trcolor44,'trcolor45':trcolor45,'trcolor46':trcolor46,'trcolor47':trcolor47,'trcolor48':trcolor48,

                            'bmrcolor1':bmrcolor1,'bmrcolor2':bmrcolor2,'bmrcolor3':bmrcolor3,'bmrcolor4':bmrcolor4,'bmrcolor5':bmrcolor5,'bmrcolor6':bmrcolor6,'bmrcolor7':bmrcolor7,
                            'bmrcolor8':bmrcolor8,'bmrcolor9':bmrcolor9,'bmrcolor10':bmrcolor10,'bmrcolor11':bmrcolor11,'bmrcolor12':bmrcolor12,'bmrcolor13':bmrcolor13,
                            'bmrcolor14':bmrcolor14,'bmrcolor15':bmrcolor15,'bmrcolor16':bmrcolor16,'bmrcolor17':bmrcolor17,'bmrcolor18':bmrcolor18,'bmrcolor19':bmrcolor19,
                            'bmrcolor20':bmrcolor20,'bmrcolor21':bmrcolor21,'bmrcolor22':bmrcolor22,'bmrcolor23':bmrcolor23,'bmrcolor24':bmrcolor24,'bmrcolor25':bmrcolor25,
                            'bmrcolor26':bmrcolor26,'bmrcolor27':bmrcolor27,'bmrcolor28':bmrcolor28,'bmrcolor29':bmrcolor29,'bmrcolor30':bmrcolor30,'bmrcolor31':bmrcolor31,
                            'bmrcolor32':bmrcolor32,'bmrcolor33':bmrcolor33,'bmrcolor34':bmrcolor34,'bmrcolor35':bmrcolor35,'bmrcolor36':bmrcolor36,'bmrcolor37':bmrcolor37,
                            'bmrcolor38':bmrcolor38,'bmrcolor39':bmrcolor39,'bmrcolor40':bmrcolor40,'bmrcolor41':bmrcolor41,'bmrcolor42':bmrcolor42,'bmrcolor43':bmrcolor43,
                            'bmrcolor44':bmrcolor44,'bmrcolor45':bmrcolor45,'bmrcolor46':bmrcolor46,'bmrcolor47':bmrcolor47,'bmrcolor48':bmrcolor48,
                        })
                    #End of multi-access management function
        if reservationform.is_valid():
            #reservation = Reservation(**reservationform.cleaned_data,user=user)
            reservation =reservationform.save(commit=False)
            reservation.user=request.user
            if int(reservation.extraTime)>0:
                formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(hours=int(request.POST.get('extraTime')))).time())
                message = "Reservation pending till admin validates !"
                reservation.isValidated=False
                reservation.endTime=((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(hours=int(request.POST.get('extraTime')))).time())
                reservation.save()

                if reservation.date==datetime.date.today():
                                if reservation.typeOf=="Small meeting room":
                                    if str(reservation.startTime)=="00:00:00":
                                        smrcolor1=""
                                        if str(reservation.endTime)=="01:00:00":
                                            smrcolor2="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            smrcolor2="orange"
                                            smrcolor3="orange"
                                            smrcolor4="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            smrcolor2="orange"
                                            smrcolor3="orange"
                                            smrcolor4="orange"
                                            smrcolor5="orange"
                                            smrcolor6="orange"
                                    elif str(reservation.startTime)=="00:30:00":
                                        smrcolor2="orange"
                                        if str(reservation.endTime)=="01:30:00":
                                            smrcolor3="orange"
                                        if str(reservation.endTime)=="2:30:00":
                                            smrcolor3="orange"
                                            smrcolor4="orange"
                                            smrcolor5="orange"
                                        if str(reservation.endTime)=="3:30:00":
                                            smrcolor7="orange"
                                            smrcolor3="orange"
                                            smrcolor4="orange"
                                            smrcolor5="orange"
                                            smrcolor6="orange"
                                    elif str(reservation.startTime)=="01:00:00":
                                        smrcolor3="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            smrcolor4="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            smrcolor4="orange"
                                            smrcolor5="orange"
                                            smrcolor6="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            smrcolor8="orange"
                                            smrcolor7="orange"
                                            smrcolor4="orange"
                                            smrcolor5="orange"
                                            smrcolor6="orange"
                                    elif str(reservation.startTime)=="01:30:00":
                                        smrcolor4="orange"
                                        if str(reservation.endTime)=="02:30:00":
                                            smrcolor5="orange"
                                        if str(reservation.endTime)=="03:30:00":
                                            smrcolor5="orange"
                                            smrcolor6="orange"
                                            smrcolor7="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            smrcolor5="orange"
                                            smrcolor6="orange"
                                            smrcolor7="orange"
                                            smrcolor8="orange"
                                            smrcolor9="orange"
                                    elif str(reservation.startTime)=="02:00:00":
                                        smrcolor5="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            smrcolor6="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            smrcolor6="orange"
                                            smrcolor7="orange"
                                            smrcolor8="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            smrcolor10="orange"
                                            smrcolor6="orange"
                                            smrcolor7="orange"
                                            smrcolor8="orange"
                                            smrcolor9="orange"
                                    elif str(reservation.startTime)=="02:30:00":
                                        smrcolor6="orange"
                                        if str(reservation.endTime)=="03:30:00":
                                            smrcolor7="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            smrcolor9="orange"
                                            smrcolor7="orange"
                                            smrcolor8="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            smrcolor10="orange"
                                            smrcolor11="orange"
                                            smrcolor7="orange"
                                            smrcolor8="orange"
                                            smrcolor9="orange"
                                    elif str(reservation.startTime)=="03:00:00":
                                        smrcolor7="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            smrcolor8="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            smrcolor9="orange"
                                            smrcolor10="orange"
                                            smrcolor8="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor10="orange"
                                            smrcolor11="orange"
                                            smrcolor12="orange"
                                            smrcolor8="orange"
                                            smrcolor9="orange"
                                    elif str(reservation.startTime)=="03:30:00":
                                        smrcolor8="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            smrcolor9="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            smrcolor9="orange"
                                            smrcolor10="orange"
                                            smrcolor11="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            smrcolor10="orange"
                                            smrcolor11="orange"
                                            smrcolor12="orange"
                                            smrcolor13="orange"
                                            smrcolor9="orange"
                                    elif str(reservation.startTime)=="04:00:00":
                                        smrcolor9="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            smrcolor10="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor12="orange"
                                            smrcolor10="orange"
                                            smrcolor11="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            smrcolor10="orange"
                                            smrcolor11="orange"
                                            smrcolor12="orange"
                                            smrcolor13="orange"
                                            smrcolor14="orange"
                                    elif str(reservation.startTime)=="04:30:00":
                                        smrcolor10="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            smrcolor11="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            smrcolor12="orange"
                                            smrcolor13="orange"
                                            smrcolor11="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            smrcolor15="orange"
                                            smrcolor11="orange"
                                            smrcolor12="orange"
                                            smrcolor13="orange"
                                            smrcolor14="orange"
                                    elif str(reservation.startTime)=="05:00:00":
                                        smrcolor11="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor12="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            smrcolor12="orange"
                                            smrcolor13="orange"
                                            smrcolor14="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            smrcolor15="orange"
                                            smrcolor16="orange"
                                            smrcolor12="orange"
                                            smrcolor13="orange"
                                            smrcolor14="orange"
                                    elif str(reservation.startTime)=="05:30:00":
                                        smrcolor12="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            smrcolor13="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            smrcolor15="orange"
                                            smrcolor13="orange"
                                            smrcolor14="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            smrcolor15="orange"
                                            smrcolor16="orange"
                                            smrcolor17="orange"
                                            smrcolor13="orange"
                                            smrcolor14="orange"
                                    elif str(reservation.startTime)=="06:00:00":
                                        smrcolor13="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            smrcolor14="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            smrcolor15="orange"
                                            smrcolor16="orange"
                                            smrcolor14="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor15="orange"
                                            smrcolor16="orange"
                                            smrcolor17="orange"
                                            smrcolor18="orange"
                                            smrcolor14="orange"
                                    elif str(reservation.startTime)=="06:30:00":
                                        smrcolor14="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            smrcolor15="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            smrcolor15="orange"
                                            smrcolor16="orange"
                                            smrcolor17="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor15="orange"
                                            smrcolor16="orange"
                                            smrcolor17="orange"
                                            smrcolor18="orange"
                                            smrcolor19="orange"
                                    elif str(reservation.startTime)=="07:00:00":
                                        smrcolor15="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            smrcolor16="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor18="orange"
                                            smrcolor16="orange"
                                            smrcolor17="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor20="orange"
                                            smrcolor16="orange"
                                            smrcolor17="orange"
                                            smrcolor18="orange"
                                            smrcolor19="orange"
                                    elif str(reservation.startTime)=="07:30:00":
                                        smrcolor16="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            smrcolor17="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor18="orange"
                                            smrcolor19="orange"
                                            smrcolor17="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor20="orange"
                                            smrcolor21="orange"
                                            smrcolor17="orange"
                                            smrcolor18="orange"
                                            smrcolor19="orange"
                                    elif str(reservation.startTime)=="08:00:00":
                                        smrcolor17="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor18="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor18="orange"
                                            smrcolor19="orange"
                                            smrcolor20="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor20="orange"
                                            smrcolor21="orange"
                                            smrcolor22="orange"
                                            smrcolor18="orange"
                                            smrcolor19="orange"
                                    elif str(reservation.startTime)=="08:30:00":
                                        smrcolor18="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor19="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor21="orange"
                                            smrcolor19="orange"
                                            smrcolor20="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            smrcolor20="orange"
                                            smrcolor21="orange"
                                            smrcolor22="orange"
                                            smrcolor23="orange"
                                            smrcolor19="orange"
                                    elif str(reservation.startTime)=="09:00:00":
                                        smrcolor19="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor20="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor21="orange"
                                            smrcolor22="orange"
                                            smrcolor20="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor20="orange"
                                            smrcolor21="orange"
                                            smrcolor22="orange"
                                            smrcolor23="orange"
                                            smrcolor24="orange"
                                    elif str(reservation.startTime)=="09:30:00":
                                        smrcolor20="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor21="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            smrcolor21="orange"
                                            smrcolor22="orange"
                                            smrcolor23="orange"
                                        if str(reservation.endTime)=="12:30:00":
                                            smrcolor25="orange"
                                            smrcolor21="orange"
                                            smrcolor22="orange"
                                            smrcolor23="orange"
                                            smrcolor24="orange"
                                    elif str(reservation.startTime)=="10:00:00":
                                        smrcolor21="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor22="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor24="orange"
                                            smrcolor22="orange"
                                            smrcolor23="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor25="orange"
                                            smrcolor26="orange"
                                            smrcolor22="orange"
                                            smrcolor23="orange"
                                            smrcolor24="orange"
                                    elif str(reservation.startTime)=="10:30:00":
                                        smrcolor22="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor23="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor24="orange"
                                            smrcolor25="orange"
                                            smrcolor23="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor25="orange"
                                            smrcolor26="orange"
                                            smrcolor27="orange"
                                            smrcolor23="orange"
                                            smrcolor24="orange"
                                    elif str(reservation.startTime)=="11:00:00":
                                        smrcolor23="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor24="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor24="orange"
                                            smrcolor25="orange"
                                            smrcolor26="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor25="orange"
                                            smrcolor26="orange"
                                            smrcolor27="orange"
                                            smrcolor28="orange"
                                            smrcolor24="orange"
                                    elif str(reservation.startTime)=="11:30:00":
                                        smrcolor24="orange"
                                        if str(reservation.endTime)=="12:30:00":
                                            smrcolor25="orange"
                                        if str(reservation.endTime)=="13:30:00":
                                            smrcolor27="orange"
                                            smrcolor25="orange"
                                            smrcolor26="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            smrcolor25="orange"
                                            smrcolor26="orange"
                                            smrcolor27="orange"
                                            smrcolor28="orange"
                                            smrcolor29="orange"




                                    elif str(reservation.startTime)=="12:00:00":
                                        smrcolor25="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor26="orange"
                                        if str(reservation.endTime)=="14:00:00":
                                            smrcolor26="orange"
                                            smrcolor27="orange"
                                            smrcolor28="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            smrcolor26="orange"
                                            smrcolor27="orange"
                                            smrcolor28="orange"
                                            smrcolor29="orange"
                                            smrcolor30="orange"
                                    elif str(reservation.startTime)=="12:30:00":
                                        smrcolor2="orange"
                                        if str(reservation.endTime)=="13:30:00":
                                            smrcolor27="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            smrcolor27="orange"
                                            smrcolor28="orange"
                                            smrcolor29="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            smrcolor31="orange"
                                            smrcolor27="orange"
                                            smrcolor28="orange"
                                            smrcolor29="orange"
                                            smrcolor30="orange"
                                    elif str(reservation.startTime)=="13:00:00":
                                        smrcolor27="orange"
                                        if str(reservation.endTime)=="14:00:00":
                                            smrcolor28="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            smrcolor28="orange"
                                            smrcolor29="orange"
                                            smrcolor30="orange"
                                        if str(reservation.endTime)=="16:00:00":
                                            smrcolor32="orange"
                                            smrcolor31="orange"
                                            smrcolor28="orange"
                                            smrcolor29="orange"
                                            smrcolor30="orange"
                                    elif str(reservation.startTime)=="13:30:00":
                                        smrcolor28="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            smrcolor29="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            smrcolor29="orange"
                                            smrcolor30="orange"
                                            smrcolor31="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            smrcolor29="orange"
                                            smrcolor30="orange"
                                            smrcolor31="orange"
                                            smrcolor32="orange"
                                            smrcolor33="orange"
                                    elif str(reservation.startTime)=="14:00:00":
                                        smrcolor29="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            smrcolor30="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor30="orange"
                                            smrcolor31="orange"
                                            smrcolor32="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            smrcolor34="orange"
                                            smrcolor30="orange"
                                            smrcolor31="orange"
                                            smrcolor32="orange"
                                            smrcolor33="orange"
                                    elif str(reservation.startTime)=="14:30:00":
                                        smrcolor30="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            smrcolor31="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            smrcolor33="orange"
                                            smrcolor31="orange"
                                            smrcolor32="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            smrcolor34="orange"
                                            smrcolor35="orange"
                                            smrcolor31="orange"
                                            smrcolor32="orange"
                                            smrcolor33="orange"
                                    elif str(reservation.startTime)=="15:00:00":
                                        smrcolor31="orange"
                                        if str(reservation.endTime)=="16:00:00":
                                            smrcolor32="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            smrcolor33="orange"
                                            smrcolor34="orange"
                                            smrcolor32="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            smrcolor34="orange"
                                            smrcolor35="orange"
                                            smrcolor12="orange"
                                            smrcolor32="orange"
                                            smrcolor33="orange"
                                    elif str(reservation.startTime)=="15:30:00":
                                        smrcolor32="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            smrcolor33="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            smrcolor33="orange"
                                            smrcolor34="orange"
                                            smrcolor35="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            smrcolor34="orange"
                                            smrcolor35="orange"
                                            smrcolor36="orange"
                                            smrcolor37="orange"
                                            smrcolor33="orange"
                                    elif str(reservation.startTime)=="16:00:00":
                                        smrcolor33="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            smrcolor34="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            smrcolor36="orange"
                                            smrcolor34="orange"
                                            smrcolor35="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            smrcolor34="orange"
                                            smrcolor35="orange"
                                            smrcolor36="orange"
                                            smrcolor37="orange"
                                            smrcolor38="orange"
                                    elif str(reservation.startTime)=="16:30:00":
                                        smrcolor34="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            smrcolor35="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            smrcolor36="orange"
                                            smrcolor37="orange"
                                            smrcolor35="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            smrcolor39="orange"
                                            smrcolor35="orange"
                                            smrcolor36="orange"
                                            smrcolor37="orange"
                                            smrcolor38="orange"
                                    elif str(reservation.startTime)=="17:00:00":
                                        smrcolor35="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            smrcolor36="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            smrcolor36="orange"
                                            smrcolor37="orange"
                                            smrcolor38="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            smrcolor39="orange"
                                            smrcolor40="orange"
                                            smrcolor36="orange"
                                            smrcolor37="orange"
                                            smrcolor38="orange"
                                    elif str(reservation.startTime)=="17:30:00":
                                        smrcolor36="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            smrcolor37="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            smrcolor39="orange"
                                            smrcolor37="orange"
                                            smrcolor38="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            smrcolor39="orange"
                                            smrcolor40="orange"
                                            smrcolor41="orange"
                                            smrcolor37="orange"
                                            smrcolor38="orange"
                                    elif str(reservation.startTime)=="18:00:00":
                                        smrcolor37="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            smrcolor38="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            smrcolor39="orange"
                                            smrcolor40="orange"
                                            smrcolor38="orange"
                                        if str(reservation.endTime)=="21:00:00":
                                            smrcolor39="orange"
                                            smrcolor40="orange"
                                            smrcolor41="orange"
                                            smrcolor42="orange"
                                            smrcolor38="orange"
                                    elif str(reservation.startTime)=="18:30:00":
                                        smrcolor38="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            smrcolor39="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            smrcolor39="orange"
                                            smrcolor40="orange"
                                            smrcolor41="orange"
                                        if str(reservation.endTime)=="21:30:00":
                                            smrcolor39="orange"
                                            smrcolor40="orange"
                                            smrcolor41="orange"
                                            smrcolor42="orange"
                                            smrcolor43="orange"
                                    elif str(reservation.startTime)=="19:00:00":
                                        smrcolor39="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            smrcolor40="orange"
                                        if str(reservation.endTime)=="21:00:00":
                                            smrcolor42="orange"
                                            smrcolor40="orange"
                                            smrcolor41="orange"
                                        if str(reservation.endTime)=="22:00:00":
                                            smrcolor44="orange"
                                            smrcolor40="orange"
                                            smrcolor41="orange"
                                            smrcolor42="orange"
                                            smrcolor43="orange"
                                    elif str(reservation.startTime)=="19:30:00":
                                        smrcolor40="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            smrcolor41="orange"
                                        if str(reservation.endTime)=="21:30:00":
                                            smrcolor42="orange"
                                            smrcolor43="orange"
                                            smrcolor41="orange"
                                        if str(reservation.endTime)=="22:30:00":
                                            smrcolor44="orange"
                                            smrcolor45="orange"
                                            smrcolor41="orange"
                                            smrcolor42="orange"
                                            smrcolor43="orange"
                                    elif str(reservation.startTime)=="08:00:00":
                                        smrcolor41="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor42="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor42="orange"
                                            smrcolor43="orange"
                                            smrcolor44="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor44="orange"
                                            smrcolor45="orange"
                                            smrcolor46="orange"
                                            smrcolor42="orange"
                                            smrcolor43="orange"
                                    elif str(reservation.startTime)=="08:30:00":
                                        smrcolor42="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor43="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor45="orange"
                                            smrcolor43="orange"
                                            smrcolor44="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            smrcolor44="orange"
                                            smrcolor45="orange"
                                            smrcolor46="orange"
                                            smrcolor47="orange"
                                            smrcolor43="orange"
                                    elif str(reservation.startTime)=="21:00:00":
                                        smrcolor43="orange"
                                        if str(reservation.endTime)=="22:00:00":
                                            smrcolor44="orange"
                                        if str(reservation.endTime)=="23:00:00":
                                            smrcolor45="orange"
                                            smrcolor46="orange"
                                            smrcolor44="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            smrcolor44="orange"
                                            smrcolor45="orange"
                                            smrcolor46="orange"
                                            smrcolor47="orange"
                                            smrcolor48="orange"
                                    elif str(reservation.startTime)=="21:30:00":
                                        smrcolor44="orange"
                                        if str(reservation.endTime)=="22:30:00":
                                            smrcolor45="orange"
                                        if str(reservation.endTime)=="23:30:00":
                                            smrcolor45="orange"
                                            smrcolor46="orange"
                                            smrcolor47="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            #smrcolor25="orange"
                                            smrcolor45="orange"
                                            smrcolor46="orange"
                                            smrcolor47="orange"
                                            smrcolor48="orange"
                                    elif str(reservation.startTime)=="22:00:00":
                                        smrcolor45="orange"
                                        if str(reservation.endTime)=="23:00:00":
                                            smrcolor46="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            smrcolor48="orange"
                                            smrcolor46="orange"
                                            smrcolor47="orange"
                                        if str(reservation.endTime)=="1:00:00":
                                            #smrcolor25="orange"
                                            #smrcolor26="orange"
                                            smrcolor46="orange"
                                            smrcolor47="orange"
                                            smrcolor48="orange"
                                    elif str(reservation.startTime)=="22:30:00":
                                        smrcolor46="orange"
                                        if str(reservation.endTime)=="23:30:00":
                                            smrcolor47="orange"
                                        if str(reservation.endTime)=="00:30:00":
                                            smrcolor48="orange"
                                            #smrcolor25="orange"
                                            smrcolor47="orange"
                                        if str(reservation.endTime)=="01:30:00":
                                            #smrcolor25="orange"
                                            #smrcolor26="orange"
                                            #smrcolor27="orange"
                                            smrcolor47="orange"
                                            smrcolor48="orange"
                                    elif str(reservation.startTime)=="23:00:00":
                                        smrcolor47="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            smrcolor48="orange"
                                        if str(reservation.endTime)=="01:00:00":
                                            smrcolor48="orange"
                                            #smrcolor25="orange"
                                            #smrcolor26="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            #smrcolor25="orange"
                                            #smrcolor26="orange"
                                            #smrcolor27="orange"
                                            #smrcolor28="orange"
                                            smrcolor48="orange"
                                    elif str(reservation.startTime)=="23:30:00":
                                        smrcolor48="orange"
                                        #if str(reservation.endTime)=="00:30:00":
                                            #smrcolor25="orange"
                                        #elif str(reservation.endTime)=="01:30:00":
                                            #smrcolor27="orange"
                                            #smrcolor25="orange"
                                            #smrcolor26="orange"
                                        #elif str(reservation.endTime)=="02:30:00":
                                            #smrcolor25="orange"
                                            #smrcolor26="orange"
                                            #smrcolor27="orange"
                                            #smrcolor28="orange"
                                            #smrcolor29="orange"
                                elif reservation.typeOf=="Training Room":
                                    if str(reservation.startTime)=="00:00:00":
                                        trcolor1="orange"
                                        if str(reservation.endTime)=="01:00:00":
                                            trcolor2="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            trcolor2="orange"
                                            trcolor3="orange"
                                            trcolor4="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            trcolor2="orange"
                                            trcolor3="orange"
                                            trcolor4="orange"
                                            trcolor5="orange"
                                            trcolor6="orange"
                                    elif str(reservation.startTime)=="00:30:00":
                                        trcolor2="orange"
                                        if str(reservation.endTime)=="01:30:00":
                                            trcolor3="orange"
                                        if str(reservation.endTime)=="2:30:00":
                                            trcolor3="orange"
                                            trcolor4="orange"
                                            trcolor5="orange"
                                        if str(reservation.endTime)=="3:30:00":
                                            trcolor7="orange"
                                            trcolor3="orange"
                                            trcolor4="orange"
                                            trcolor5="orange"
                                            trcolor6="orange"
                                    elif str(reservation.startTime)=="01:00:00":
                                        trcolor3="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            trcolor4="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            trcolor4="orange"
                                            trcolor5="orange"
                                            trcolor6="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            trcolor8="orange"
                                            trcolor7="orange"
                                            trcolor4="orange"
                                            trcolor5="orange"
                                            trcolor6="orange"
                                    elif str(reservation.startTime)=="01:30:00":
                                        trcolor4="orange"
                                        if str(reservation.endTime)=="02:30:00":
                                            trcolor5="orange"
                                        if str(reservation.endTime)=="03:30:00":
                                            trcolor5="orange"
                                            trcolor6="orange"
                                            trcolor7="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            trcolor5="orange"
                                            trcolor6="orange"
                                            trcolor7="orange"
                                            trcolor8="orange"
                                            trcolor9="orange"
                                    elif str(reservation.startTime)=="02:00:00":
                                        trcolor5="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            trcolor6="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            trcolor6="orange"
                                            trcolor7="orange"
                                            trcolor8="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            trcolor10="orange"
                                            trcolor6="orange"
                                            trcolor7="orange"
                                            trcolor8="orange"
                                            trcolor9="orange"
                                    elif str(reservation.startTime)=="02:30:00":
                                        trcolor6="orange"
                                        if str(reservation.endTime)=="03:30:00":
                                            trcolor7="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            trcolor9="orange"
                                            trcolor7="orange"
                                            trcolor8="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            trcolor10="orange"
                                            trcolor11="orange"
                                            trcolor7="orange"
                                            trcolor8="orange"
                                            trcolor9="orange"
                                    elif str(reservation.startTime)=="03:00:00":
                                        trcolor7="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            trcolor8="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            trcolor9="orange"
                                            trcolor10="orange"
                                            trcolor8="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor10="orange"
                                            trcolor11="orange"
                                            trcolor12="orange"
                                            trcolor8="orange"
                                            trcolor9="orange"
                                    elif str(reservation.startTime)=="03:30:00":
                                        trcolor8="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            trcolor9="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            trcolor9="orange"
                                            trcolor10="orange"
                                            trcolor11="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            trcolor10="orange"
                                            trcolor11="orange"
                                            trcolor12="orange"
                                            trcolor13="orange"
                                            trcolor9="orange"
                                    elif str(reservation.startTime)=="04:00:00":
                                        trcolor9="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            trcolor10="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor12="orange"
                                            trcolor10="orange"
                                            trcolor11="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            trcolor10="orange"
                                            trcolor11="orange"
                                            trcolor12="orange"
                                            trcolor13="orange"
                                            trcolor14="orange"
                                    elif str(reservation.startTime)=="04:30:00":
                                        trcolor10="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            trcolor11="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            trcolor12="orange"
                                            trcolor13="orange"
                                            trcolor11="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            trcolor15="orange"
                                            trcolor11="orange"
                                            trcolor12="orange"
                                            trcolor13="orange"
                                            trcolor14="orange"
                                    elif str(reservation.startTime)=="05:00:00":
                                        trcolor11="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor12="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            trcolor12="orange"
                                            trcolor13="orange"
                                            trcolor14="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            trcolor15="orange"
                                            trcolor16="orange"
                                            trcolor12="orange"
                                            trcolor13="orange"
                                            trcolor14="orange"
                                    elif str(reservation.startTime)=="05:30:00":
                                        trcolor12="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            trcolor13="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            trcolor15="orange"
                                            trcolor13="orange"
                                            trcolor14="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            trcolor15="orange"
                                            trcolor16="orange"
                                            trcolor17="orange"
                                            trcolor13="orange"
                                            trcolor14="orange"
                                    elif str(reservation.startTime)=="06:00:00":
                                        trcolor13="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            trcolor14="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            trcolor15="orange"
                                            trcolor16="orange"
                                            trcolor14="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor15="orange"
                                            trcolor16="orange"
                                            trcolor17="orange"
                                            trcolor18="orange"
                                            trcolor14="orange"
                                    elif str(reservation.startTime)=="06:30:00":
                                        trcolor14="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            trcolor15="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            trcolor15="orange"
                                            trcolor16="orange"
                                            trcolor17="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor15="orange"
                                            trcolor16="orange"
                                            trcolor17="orange"
                                            trcolor18="orange"
                                            trcolor19="orange"
                                    elif str(reservation.startTime)=="07:00:00":
                                        trcolor15="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            trcolor16="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor18="orange"
                                            trcolor16="orange"
                                            trcolor17="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor20="orange"
                                            trcolor16="orange"
                                            trcolor17="orange"
                                            trcolor18="orange"
                                            trcolor19="orange"
                                    elif str(reservation.startTime)=="07:30:00":
                                        trcolor16="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            trcolor17="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor18="orange"
                                            trcolor19="orange"
                                            trcolor17="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor20="orange"
                                            trcolor21="orange"
                                            trcolor17="orange"
                                            trcolor18="orange"
                                            trcolor19="orange"
                                    elif str(reservation.startTime)=="08:00:00":
                                        trcolor17="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor18="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor18="orange"
                                            trcolor19="orange"
                                            trcolor20="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor20="orange"
                                            trcolor21="orange"
                                            trcolor22="orange"
                                            trcolor18="orange"
                                            trcolor19="orange"
                                    elif str(reservation.startTime)=="08:30:00":
                                        trcolor18="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor19="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor21="orange"
                                            trcolor19="orange"
                                            trcolor20="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            trcolor20="orange"
                                            trcolor21="orange"
                                            trcolor22="orange"
                                            trcolor23="orange"
                                            trcolor19="orange"
                                    elif str(reservation.startTime)=="09:00:00":
                                        trcolor19="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor20="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor21="orange"
                                            trcolor22="orange"
                                            trcolor20="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor20="orange"
                                            trcolor21="orange"
                                            trcolor22="orange"
                                            trcolor23="orange"
                                            trcolor24="orange"
                                    elif str(reservation.startTime)=="09:30:00":
                                        trcolor20="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor21="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            trcolor21="orange"
                                            trcolor22="orange"
                                            trcolor23="orange"
                                        if str(reservation.endTime)=="12:30:00":
                                            trcolor25="orange"
                                            trcolor21="orange"
                                            trcolor22="orange"
                                            trcolor23="orange"
                                            trcolor24="orange"
                                    elif str(reservation.startTime)=="10:00:00":
                                        trcolor21="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor22="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor24="orange"
                                            trcolor22="orange"
                                            trcolor23="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor25="orange"
                                            trcolor26="orange"
                                            trcolor22="orange"
                                            trcolor23="orange"
                                            trcolor24="orange"
                                    elif str(reservation.startTime)=="10:30:00":
                                        trcolor22="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor23="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor24="orange"
                                            trcolor25="orange"
                                            trcolor23="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor25="orange"
                                            trcolor26="orange"
                                            trcolor27="orange"
                                            trcolor23="orange"
                                            trcolor24="orange"
                                    elif str(reservation.startTime)=="11:00:00":
                                        trcolor23="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor24="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor24="orange"
                                            trcolor25="orange"
                                            trcolor26="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor25="orange"
                                            trcolor26="orange"
                                            trcolor27="orange"
                                            trcolor28="orange"
                                            trcolor24="orange"
                                    elif str(reservation.startTime)=="11:30:00":
                                        trcolor24="orange"
                                        if str(reservation.endTime)=="12:30:00":
                                            trcolor25="orange"
                                        if str(reservation.endTime)=="13:30:00":
                                            trcolor27="orange"
                                            trcolor25="orange"
                                            trcolor26="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            trcolor25="orange"
                                            trcolor26="orange"
                                            trcolor27="orange"
                                            trcolor28="orange"
                                            trcolor29="orange"




                                    elif str(reservation.startTime)=="12:00:00":
                                        trcolor25="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor26="orange"
                                        if str(reservation.endTime)=="14:00:00":
                                            trcolor26="orange"
                                            trcolor27="orange"
                                            trcolor28="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            trcolor26="orange"
                                            trcolor27="orange"
                                            trcolor28="orange"
                                            trcolor29="orange"
                                            trcolor30="orange"
                                    elif str(reservation.startTime)=="12:30:00":
                                        trcolor2="orange"
                                        if str(reservation.endTime)=="13:30:00":
                                            trcolor27="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            trcolor27="orange"
                                            trcolor28="orange"
                                            trcolor29="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            trcolor31="orange"
                                            trcolor27="orange"
                                            trcolor28="orange"
                                            trcolor29="orange"
                                            trcolor30="orange"
                                    elif str(reservation.startTime)=="13:00:00":
                                        trcolor27="orange"
                                        if str(reservation.endTime)=="14:00:00":
                                            trcolor28="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            trcolor28="orange"
                                            trcolor29="orange"
                                            trcolor30="orange"
                                        if str(reservation.endTime)=="16:00:00":
                                            trcolor32="orange"
                                            trcolor31="orange"
                                            trcolor28="orange"
                                            trcolor29="orange"
                                            trcolor30="orange"
                                    elif str(reservation.startTime)=="13:30:00":
                                        trcolor28="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            trcolor29="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            trcolor29="orange"
                                            trcolor30="orange"
                                            trcolor31="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            trcolor29="orange"
                                            trcolor30="orange"
                                            trcolor31="orange"
                                            trcolor32="orange"
                                            trcolor33="orange"
                                    elif str(reservation.startTime)=="14:00:00":
                                        trcolor29="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            trcolor30="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor30="orange"
                                            trcolor31="orange"
                                            trcolor32="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            trcolor34="orange"
                                            trcolor30="orange"
                                            trcolor31="orange"
                                            trcolor32="orange"
                                            trcolor33="orange"
                                    elif str(reservation.startTime)=="14:30:00":
                                        trcolor30="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            trcolor31="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            trcolor33="orange"
                                            trcolor31="orange"
                                            trcolor32="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            trcolor34="orange"
                                            trcolor35="orange"
                                            trcolor31="orange"
                                            trcolor32="orange"
                                            trcolor33="orange"
                                    elif str(reservation.startTime)=="15:00:00":
                                        trcolor31="orange"
                                        if str(reservation.endTime)=="16:00:00":
                                            trcolor32="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            trcolor33="orange"
                                            trcolor34="orange"
                                            trcolor32="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            trcolor34="orange"
                                            trcolor35="orange"
                                            trcolor12="orange"
                                            trcolor32="orange"
                                            trcolor33="orange"
                                    elif str(reservation.startTime)=="15:30:00":
                                        trcolor32="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            trcolor33="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            trcolor33="orange"
                                            trcolor34="orange"
                                            trcolor35="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            trcolor34="orange"
                                            trcolor35="orange"
                                            trcolor36="orange"
                                            trcolor37="orange"
                                            trcolor33="orange"
                                    elif str(reservation.startTime)=="16:00:00":
                                        trcolor33="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            trcolor34="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            trcolor36="orange"
                                            trcolor34="orange"
                                            trcolor35="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            trcolor34="orange"
                                            trcolor35="orange"
                                            trcolor36="orange"
                                            trcolor37="orange"
                                            trcolor38="orange"
                                    elif str(reservation.startTime)=="16:30:00":
                                        trcolor34="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            trcolor35="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            trcolor36="orange"
                                            trcolor37="orange"
                                            trcolor35="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            trcolor39="orange"
                                            trcolor35="orange"
                                            trcolor36="orange"
                                            trcolor37="orange"
                                            trcolor38="orange"
                                    elif str(reservation.startTime)=="17:00:00":
                                        trcolor35="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            trcolor36="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            trcolor36="orange"
                                            trcolor37="orange"
                                            trcolor38="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            trcolor39="orange"
                                            trcolor40="orange"
                                            trcolor36="orange"
                                            trcolor37="orange"
                                            trcolor38="orange"
                                    elif str(reservation.startTime)=="17:30:00":
                                        trcolor36="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            trcolor37="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            trcolor39="orange"
                                            trcolor37="orange"
                                            trcolor38="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            trcolor39="orange"
                                            trcolor40="orange"
                                            trcolor41="orange"
                                            trcolor37="orange"
                                            trcolor38="orange"
                                    elif str(reservation.startTime)=="18:00:00":
                                        trcolor37="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            trcolor38="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            trcolor39="orange"
                                            trcolor40="orange"
                                            trcolor38="orange"
                                        if str(reservation.endTime)=="21:00:00":
                                            trcolor39="orange"
                                            trcolor40="orange"
                                            trcolor41="orange"
                                            trcolor42="orange"
                                            trcolor38="orange"
                                    elif str(reservation.startTime)=="18:30:00":
                                        trcolor38="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            trcolor39="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            trcolor39="orange"
                                            trcolor40="orange"
                                            trcolor41="orange"
                                        if str(reservation.endTime)=="21:30:00":
                                            trcolor39="orange"
                                            trcolor40="orange"
                                            trcolor41="orange"
                                            trcolor42="orange"
                                            trcolor43="orange"
                                    elif str(reservation.startTime)=="19:00:00":
                                        trcolor39="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            trcolor40="orange"
                                        if str(reservation.endTime)=="21:00:00":
                                            trcolor42="orange"
                                            trcolor40="orange"
                                            trcolor41="orange"
                                        if str(reservation.endTime)=="22:00:00":
                                            trcolor44="orange"
                                            trcolor40="orange"
                                            trcolor41="orange"
                                            trcolor42="orange"
                                            trcolor43="orange"
                                    elif str(reservation.startTime)=="19:30:00":
                                        trcolor40="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            trcolor41="orange"
                                        if str(reservation.endTime)=="21:30:00":
                                            trcolor42="orange"
                                            trcolor43="orange"
                                            trcolor41="orange"
                                        if str(reservation.endTime)=="22:30:00":
                                            trcolor44="orange"
                                            trcolor45="orange"
                                            trcolor41="orange"
                                            trcolor42="orange"
                                            trcolor43="orange"
                                    elif str(reservation.startTime)=="08:00:00":
                                        trcolor41="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor42="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor42="orange"
                                            trcolor43="orange"
                                            trcolor44="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor44="orange"
                                            trcolor45="orange"
                                            trcolor46="orange"
                                            trcolor42="orange"
                                            trcolor43="orange"
                                    elif str(reservation.startTime)=="08:30:00":
                                        trcolor42="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor43="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor45="orange"
                                            trcolor43="orange"
                                            trcolor44="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            trcolor44="orange"
                                            trcolor45="orange"
                                            trcolor46="orange"
                                            trcolor47="orange"
                                            trcolor43="orange"
                                    elif str(reservation.startTime)=="21:00:00":
                                        trcolor43="orange"
                                        if str(reservation.endTime)=="22:00:00":
                                            trcolor44="orange"
                                        if str(reservation.endTime)=="23:00:00":
                                            trcolor45="orange"
                                            trcolor46="orange"
                                            trcolor44="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            trcolor44="orange"
                                            trcolor45="orange"
                                            trcolor46="orange"
                                            trcolor47="orange"
                                            trcolor48="orange"
                                    elif str(reservation.startTime)=="21:30:00":
                                        trcolor44="orange"
                                        if str(reservation.endTime)=="22:30:00":
                                            trcolor45="orange"
                                        if str(reservation.endTime)=="23:30:00":
                                            trcolor45="orange"
                                            trcolor46="orange"
                                            trcolor47="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            #trcolor25="orange"
                                            trcolor45="orange"
                                            trcolor46="orange"
                                            trcolor47="orange"
                                            trcolor48="orange"
                                    elif str(reservation.startTime)=="22:00:00":
                                        trcolor45="orange"
                                        if str(reservation.endTime)=="23:00:00":
                                            trcolor46="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            trcolor48="orange"
                                            trcolor46="orange"
                                            trcolor47="orange"
                                        if str(reservation.endTime)=="1:00:00":
                                            #trcolor25="orange"
                                            #trcolor26="orange"
                                            trcolor46="orange"
                                            trcolor47="orange"
                                            trcolor48="orange"
                                    elif str(reservation.startTime)=="22:30:00":
                                        trcolor46="orange"
                                        if str(reservation.endTime)=="23:30:00":
                                            trcolor47="orange"
                                        if str(reservation.endTime)=="00:30:00":
                                            trcolor48="orange"
                                            #trcolor25="orange"
                                            trcolor47="orange"
                                        if str(reservation.endTime)=="01:30:00":
                                            #trcolor25="orange"
                                            #trcolor26="orange"
                                            #trcolor27="orange"
                                            trcolor47="orange"
                                            trcolor48="orange"
                                    elif str(reservation.startTime)=="23:00:00":
                                        trcolor47="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            trcolor48="orange"
                                        if str(reservation.endTime)=="01:00:00":
                                            trcolor48="orange"
                                            #trcolor25="orange"
                                            #trcolor26="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            #trcolor25="orange"
                                            #trcolor26="orange"
                                            #trcolor27="orange"
                                            #trcolor28="orange"
                                            trcolor48="orange"
                                    elif str(reservation.startTime)=="23:30:00":
                                        trcolor48="orange"
                                        #if str(reservation.endTime)=="00:30:00":
                                            #trcolor25="orange"
                                        #elif str(reservation.endTime)=="01:30:00":
                                            #trcolor27="orange"
                                            #trcolor25="orange"
                                            #trcolor26="orange"
                                        #elif str(reservation.endTime)=="02:30:00":
                                            #trcolor25="orange"
                                            #trcolor26="orange"
                                            #trcolor27="orange"
                                            #trcolor28="orange"
                                            #trcolor29="orange"
                                elif reservation.typeOf=="Big meeting room":
                                    if str(reservation.startTime)=="00:00:00":
                                        bmrcolor1="orange"
                                        if str(reservation.endTime)=="01:00:00":
                                            bmrcolor2="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            bmrcolor2="orange"
                                            bmrcolor3="orange"
                                            bmrcolor4="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            bmrcolor2="orange"
                                            bmrcolor3="orange"
                                            bmrcolor4="orange"
                                            bmrcolor5="orange"
                                            bmrcolor6="orange"
                                    elif str(reservation.startTime)=="00:30:00":
                                        bmrcolor2="orange"
                                        if str(reservation.endTime)=="01:30:00":
                                            bmrcolor3="orange"
                                        if str(reservation.endTime)=="2:30:00":
                                            bmrcolor3="orange"
                                            bmrcolor4="orange"
                                            bmrcolor5="orange"
                                        if str(reservation.endTime)=="3:30:00":
                                            bmrcolor7="orange"
                                            bmrcolor3="orange"
                                            bmrcolor4="orange"
                                            bmrcolor5="orange"
                                            bmrcolor6="orange"
                                    elif str(reservation.startTime)=="01:00:00":
                                        bmrcolor3="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            bmrcolor4="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            bmrcolor4="orange"
                                            bmrcolor5="orange"
                                            bmrcolor6="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            bmrcolor8="orange"
                                            bmrcolor7="orange"
                                            bmrcolor4="orange"
                                            bmrcolor5="orange"
                                            bmrcolor6="orange"
                                    elif str(reservation.startTime)=="01:30:00":
                                        bmrcolor4="orange"
                                        if str(reservation.endTime)=="02:30:00":
                                            bmrcolor5="orange"
                                        if str(reservation.endTime)=="03:30:00":
                                            bmrcolor5="orange"
                                            bmrcolor6="orange"
                                            bmrcolor7="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            bmrcolor5="orange"
                                            bmrcolor6="orange"
                                            bmrcolor7="orange"
                                            bmrcolor8="orange"
                                            bmrcolor9="orange"
                                    elif str(reservation.startTime)=="02:00:00":
                                        bmrcolor5="orange"
                                        if str(reservation.endTime)=="03:00:00":
                                            bmrcolor6="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            bmrcolor6="orange"
                                            bmrcolor7="orange"
                                            bmrcolor8="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            bmrcolor10="orange"
                                            bmrcolor6="orange"
                                            bmrcolor7="orange"
                                            bmrcolor8="orange"
                                            bmrcolor9="orange"
                                    elif str(reservation.startTime)=="02:30:00":
                                        bmrcolor6="orange"
                                        if str(reservation.endTime)=="03:30:00":
                                            bmrcolor7="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            bmrcolor9="orange"
                                            bmrcolor7="orange"
                                            bmrcolor8="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            bmrcolor10="orange"
                                            bmrcolor11="orange"
                                            bmrcolor7="orange"
                                            bmrcolor8="orange"
                                            bmrcolor9="orange"
                                    elif str(reservation.startTime)=="03:00:00":
                                        bmrcolor7="orange"
                                        if str(reservation.endTime)=="04:00:00":
                                            bmrcolor8="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            bmrcolor9="orange"
                                            bmrcolor10="orange"
                                            bmrcolor8="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor10="orange"
                                            bmrcolor11="orange"
                                            bmrcolor12="orange"
                                            bmrcolor8="orange"
                                            bmrcolor9="orange"
                                    elif str(reservation.startTime)=="03:30:00":
                                        bmrcolor8="orange"
                                        if str(reservation.endTime)=="04:30:00":
                                            bmrcolor9="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            bmrcolor9="orange"
                                            bmrcolor10="orange"
                                            bmrcolor11="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            bmrcolor10="orange"
                                            bmrcolor11="orange"
                                            bmrcolor12="orange"
                                            bmrcolor13="orange"
                                            bmrcolor9="orange"
                                    elif str(reservation.startTime)=="04:00:00":
                                        bmrcolor9="orange"
                                        if str(reservation.endTime)=="05:00:00":
                                            bmrcolor10="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor12="orange"
                                            bmrcolor10="orange"
                                            bmrcolor11="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            bmrcolor10="orange"
                                            bmrcolor11="orange"
                                            bmrcolor12="orange"
                                            bmrcolor13="orange"
                                            bmrcolor14="orange"
                                    elif str(reservation.startTime)=="04:30:00":
                                        bmrcolor10="orange"
                                        if str(reservation.endTime)=="05:30:00":
                                            bmrcolor11="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            bmrcolor12="orange"
                                            bmrcolor13="orange"
                                            bmrcolor11="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            bmrcolor15="orange"
                                            bmrcolor11="orange"
                                            bmrcolor12="orange"
                                            bmrcolor13="orange"
                                            bmrcolor14="orange"
                                    elif str(reservation.startTime)=="05:00:00":
                                        bmrcolor11="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor12="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            bmrcolor12="orange"
                                            bmrcolor13="orange"
                                            bmrcolor14="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            bmrcolor15="orange"
                                            bmrcolor16="orange"
                                            bmrcolor12="orange"
                                            bmrcolor13="orange"
                                            bmrcolor14="orange"
                                    elif str(reservation.startTime)=="05:30:00":
                                        bmrcolor12="orange"
                                        if str(reservation.endTime)=="06:30:00":
                                            bmrcolor13="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            bmrcolor15="orange"
                                            bmrcolor13="orange"
                                            bmrcolor14="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            bmrcolor15="orange"
                                            bmrcolor16="orange"
                                            bmrcolor17="orange"
                                            bmrcolor13="orange"
                                            bmrcolor14="orange"
                                    elif str(reservation.startTime)=="06:00:00":
                                        bmrcolor13="orange"
                                        if str(reservation.endTime)=="07:00:00":
                                            bmrcolor14="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            bmrcolor15="orange"
                                            bmrcolor16="orange"
                                            bmrcolor14="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor15="orange"
                                            bmrcolor16="orange"
                                            bmrcolor17="orange"
                                            bmrcolor18="orange"
                                            bmrcolor14="orange"
                                    elif str(reservation.startTime)=="06:30:00":
                                        bmrcolor14="orange"
                                        if str(reservation.endTime)=="07:30:00":
                                            bmrcolor15="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            bmrcolor15="orange"
                                            bmrcolor16="orange"
                                            bmrcolor17="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor15="orange"
                                            bmrcolor16="orange"
                                            bmrcolor17="orange"
                                            bmrcolor18="orange"
                                            bmrcolor19="orange"
                                    elif str(reservation.startTime)=="07:00:00":
                                        bmrcolor15="orange"
                                        if str(reservation.endTime)=="08:00:00":
                                            bmrcolor16="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor18="orange"
                                            bmrcolor16="orange"
                                            bmrcolor17="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor20="orange"
                                            bmrcolor16="orange"
                                            bmrcolor17="orange"
                                            bmrcolor18="orange"
                                            bmrcolor19="orange"
                                    elif str(reservation.startTime)=="07:30:00":
                                        bmrcolor16="orange"
                                        if str(reservation.endTime)=="08:30:00":
                                            bmrcolor17="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor18="orange"
                                            bmrcolor19="orange"
                                            bmrcolor17="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor20="orange"
                                            bmrcolor21="orange"
                                            bmrcolor17="orange"
                                            bmrcolor18="orange"
                                            bmrcolor19="orange"
                                    elif str(reservation.startTime)=="08:00:00":
                                        bmrcolor17="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor18="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor18="orange"
                                            bmrcolor19="orange"
                                            bmrcolor20="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor20="orange"
                                            bmrcolor21="orange"
                                            bmrcolor22="orange"
                                            bmrcolor18="orange"
                                            bmrcolor19="orange"
                                    elif str(reservation.startTime)=="08:30:00":
                                        bmrcolor18="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor19="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor21="orange"
                                            bmrcolor19="orange"
                                            bmrcolor20="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            bmrcolor20="orange"
                                            bmrcolor21="orange"
                                            bmrcolor22="orange"
                                            bmrcolor23="orange"
                                            bmrcolor19="orange"
                                    elif str(reservation.startTime)=="09:00:00":
                                        bmrcolor19="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor20="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor21="orange"
                                            bmrcolor22="orange"
                                            bmrcolor20="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor20="orange"
                                            bmrcolor21="orange"
                                            bmrcolor22="orange"
                                            bmrcolor23="orange"
                                            bmrcolor24="orange"
                                    elif str(reservation.startTime)=="09:30:00":
                                        bmrcolor20="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor21="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            bmrcolor21="orange"
                                            bmrcolor22="orange"
                                            bmrcolor23="orange"
                                        if str(reservation.endTime)=="12:30:00":
                                            bmrcolor25="orange"
                                            bmrcolor21="orange"
                                            bmrcolor22="orange"
                                            bmrcolor23="orange"
                                            bmrcolor24="orange"
                                    elif str(reservation.startTime)=="10:00:00":
                                        bmrcolor21="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor22="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor24="orange"
                                            bmrcolor22="orange"
                                            bmrcolor23="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor25="orange"
                                            bmrcolor26="orange"
                                            bmrcolor22="orange"
                                            bmrcolor23="orange"
                                            bmrcolor24="orange"
                                    elif str(reservation.startTime)=="10:30:00":
                                        bmrcolor22="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor23="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor24="orange"
                                            bmrcolor25="orange"
                                            bmrcolor23="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor25="orange"
                                            bmrcolor26="orange"
                                            bmrcolor27="orange"
                                            bmrcolor23="orange"
                                            bmrcolor24="orange"
                                    elif str(reservation.startTime)=="11:00:00":
                                        bmrcolor23="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor24="orange"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor24="orange"
                                            bmrcolor25="orange"
                                            bmrcolor26="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor25="orange"
                                            bmrcolor26="orange"
                                            bmrcolor27="orange"
                                            bmrcolor28="orange"
                                            bmrcolor24="orange"
                                    elif str(reservation.startTime)=="11:30:00":
                                        bmrcolor24="orange"
                                        if str(reservation.endTime)=="12:30:00":
                                            bmrcolor25="orange"
                                        if str(reservation.endTime)=="13:30:00":
                                            bmrcolor27="orange"
                                            bmrcolor25="orange"
                                            bmrcolor26="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            bmrcolor25="orange"
                                            bmrcolor26="orange"
                                            bmrcolor27="orange"
                                            bmrcolor28="orange"
                                            bmrcolor29="orange"




                                    elif str(reservation.startTime)=="12:00:00":
                                        bmrcolor25="orange"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor26="orange"
                                        if str(reservation.endTime)=="14:00:00":
                                            bmrcolor26="orange"
                                            bmrcolor27="orange"
                                            bmrcolor28="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            bmrcolor26="orange"
                                            bmrcolor27="orange"
                                            bmrcolor28="orange"
                                            bmrcolor29="orange"
                                            bmrcolor30="orange"
                                    elif str(reservation.startTime)=="12:30:00":
                                        bmrcolor2="orange"
                                        if str(reservation.endTime)=="13:30:00":
                                            bmrcolor27="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            bmrcolor27="orange"
                                            bmrcolor28="orange"
                                            bmrcolor29="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            bmrcolor31="orange"
                                            bmrcolor27="orange"
                                            bmrcolor28="orange"
                                            bmrcolor29="orange"
                                            bmrcolor30="orange"
                                    elif str(reservation.startTime)=="13:00:00":
                                        bmrcolor27="orange"
                                        if str(reservation.endTime)=="14:00:00":
                                            bmrcolor28="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            bmrcolor28="orange"
                                            bmrcolor29="orange"
                                            bmrcolor30="orange"
                                        if str(reservation.endTime)=="16:00:00":
                                            bmrcolor32="orange"
                                            bmrcolor31="orange"
                                            bmrcolor28="orange"
                                            bmrcolor29="orange"
                                            bmrcolor30="orange"
                                    elif str(reservation.startTime)=="13:30:00":
                                        bmrcolor28="orange"
                                        if str(reservation.endTime)=="14:30:00":
                                            bmrcolor29="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            bmrcolor29="orange"
                                            bmrcolor30="orange"
                                            bmrcolor31="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            bmrcolor29="orange"
                                            bmrcolor30="orange"
                                            bmrcolor31="orange"
                                            bmrcolor32="orange"
                                            bmrcolor33="orange"
                                    elif str(reservation.startTime)=="14:00:00":
                                        bmrcolor29="orange"
                                        if str(reservation.endTime)=="15:00:00":
                                            bmrcolor30="orange"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor30="orange"
                                            bmrcolor31="orange"
                                            bmrcolor32="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            bmrcolor34="orange"
                                            bmrcolor30="orange"
                                            bmrcolor31="orange"
                                            bmrcolor32="orange"
                                            bmrcolor33="orange"
                                    elif str(reservation.startTime)=="14:30:00":
                                        bmrcolor30="orange"
                                        if str(reservation.endTime)=="15:30:00":
                                            bmrcolor31="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            bmrcolor33="orange"
                                            bmrcolor31="orange"
                                            bmrcolor32="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            bmrcolor34="orange"
                                            bmrcolor35="orange"
                                            bmrcolor31="orange"
                                            bmrcolor32="orange"
                                            bmrcolor33="orange"
                                    elif str(reservation.startTime)=="15:00:00":
                                        bmrcolor31="orange"
                                        if str(reservation.endTime)=="16:00:00":
                                            bmrcolor32="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            bmrcolor33="orange"
                                            bmrcolor34="orange"
                                            bmrcolor32="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            bmrcolor34="orange"
                                            bmrcolor35="orange"
                                            bmrcolor12="orange"
                                            bmrcolor32="orange"
                                            bmrcolor33="orange"
                                    elif str(reservation.startTime)=="15:30:00":
                                        bmrcolor32="orange"
                                        if str(reservation.endTime)=="16:30:00":
                                            bmrcolor33="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            bmrcolor33="orange"
                                            bmrcolor34="orange"
                                            bmrcolor35="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            bmrcolor34="orange"
                                            bmrcolor35="orange"
                                            bmrcolor36="orange"
                                            bmrcolor37="orange"
                                            bmrcolor33="orange"
                                    elif str(reservation.startTime)=="16:00:00":
                                        bmrcolor33="orange"
                                        if str(reservation.endTime)=="17:00:00":
                                            bmrcolor34="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            bmrcolor36="orange"
                                            bmrcolor34="orange"
                                            bmrcolor35="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            bmrcolor34="orange"
                                            bmrcolor35="orange"
                                            bmrcolor36="orange"
                                            bmrcolor37="orange"
                                            bmrcolor38="orange"
                                    elif str(reservation.startTime)=="16:30:00":
                                        bmrcolor34="orange"
                                        if str(reservation.endTime)=="17:30:00":
                                            bmrcolor35="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            bmrcolor36="orange"
                                            bmrcolor37="orange"
                                            bmrcolor35="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            bmrcolor39="orange"
                                            bmrcolor35="orange"
                                            bmrcolor36="orange"
                                            bmrcolor37="orange"
                                            bmrcolor38="orange"
                                    elif str(reservation.startTime)=="17:00:00":
                                        bmrcolor35="orange"
                                        if str(reservation.endTime)=="18:00:00":
                                            bmrcolor36="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            bmrcolor36="orange"
                                            bmrcolor37="orange"
                                            bmrcolor38="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            bmrcolor39="orange"
                                            bmrcolor40="orange"
                                            bmrcolor36="orange"
                                            bmrcolor37="orange"
                                            bmrcolor38="orange"
                                    elif str(reservation.startTime)=="17:30:00":
                                        bmrcolor36="orange"
                                        if str(reservation.endTime)=="18:30:00":
                                            bmrcolor37="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            bmrcolor39="orange"
                                            bmrcolor37="orange"
                                            bmrcolor38="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            bmrcolor39="orange"
                                            bmrcolor40="orange"
                                            bmrcolor41="orange"
                                            bmrcolor37="orange"
                                            bmrcolor38="orange"
                                    elif str(reservation.startTime)=="18:00:00":
                                        bmrcolor37="orange"
                                        if str(reservation.endTime)=="19:00:00":
                                            bmrcolor38="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            bmrcolor39="orange"
                                            bmrcolor40="orange"
                                            bmrcolor38="orange"
                                        if str(reservation.endTime)=="21:00:00":
                                            bmrcolor39="orange"
                                            bmrcolor40="orange"
                                            bmrcolor41="orange"
                                            bmrcolor42="orange"
                                            bmrcolor38="orange"
                                    elif str(reservation.startTime)=="18:30:00":
                                        bmrcolor38="orange"
                                        if str(reservation.endTime)=="19:30:00":
                                            bmrcolor39="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            bmrcolor39="orange"
                                            bmrcolor40="orange"
                                            bmrcolor41="orange"
                                        if str(reservation.endTime)=="21:30:00":
                                            bmrcolor39="orange"
                                            bmrcolor40="orange"
                                            bmrcolor41="orange"
                                            bmrcolor42="orange"
                                            bmrcolor43="orange"
                                    elif str(reservation.startTime)=="19:00:00":
                                        bmrcolor39="orange"
                                        if str(reservation.endTime)=="20:00:00":
                                            bmrcolor40="orange"
                                        if str(reservation.endTime)=="21:00:00":
                                            bmrcolor42="orange"
                                            bmrcolor40="orange"
                                            bmrcolor41="orange"
                                        if str(reservation.endTime)=="22:00:00":
                                            bmrcolor44="orange"
                                            bmrcolor40="orange"
                                            bmrcolor41="orange"
                                            bmrcolor42="orange"
                                            bmrcolor43="orange"
                                    elif str(reservation.startTime)=="19:30:00":
                                        bmrcolor40="orange"
                                        if str(reservation.endTime)=="20:30:00":
                                            bmrcolor41="orange"
                                        if str(reservation.endTime)=="21:30:00":
                                            bmrcolor42="orange"
                                            bmrcolor43="orange"
                                            bmrcolor41="orange"
                                        if str(reservation.endTime)=="22:30:00":
                                            bmrcolor44="orange"
                                            bmrcolor45="orange"
                                            bmrcolor41="orange"
                                            bmrcolor42="orange"
                                            bmrcolor43="orange"
                                    elif str(reservation.startTime)=="08:00:00":
                                        bmrcolor41="orange"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor42="orange"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor42="orange"
                                            bmrcolor43="orange"
                                            bmrcolor44="orange"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor44="orange"
                                            bmrcolor45="orange"
                                            bmrcolor46="orange"
                                            bmrcolor42="orange"
                                            bmrcolor43="orange"
                                    elif str(reservation.startTime)=="08:30:00":
                                        bmrcolor42="orange"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor43="orange"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor45="orange"
                                            bmrcolor43="orange"
                                            bmrcolor44="orange"
                                        if str(reservation.endTime)=="11:30:00":
                                            bmrcolor44="orange"
                                            bmrcolor45="orange"
                                            bmrcolor46="orange"
                                            bmrcolor47="orange"
                                            bmrcolor43="orange"
                                    elif str(reservation.startTime)=="21:00:00":
                                        bmrcolor43="orange"
                                        if str(reservation.endTime)=="22:00:00":
                                            bmrcolor44="orange"
                                        if str(reservation.endTime)=="23:00:00":
                                            bmrcolor45="orange"
                                            bmrcolor46="orange"
                                            bmrcolor44="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            bmrcolor44="orange"
                                            bmrcolor45="orange"
                                            bmrcolor46="orange"
                                            bmrcolor47="orange"
                                            bmrcolor48="orange"
                                    elif str(reservation.startTime)=="21:30:00":
                                        bmrcolor44="orange"
                                        if str(reservation.endTime)=="22:30:00":
                                            bmrcolor45="orange"
                                        if str(reservation.endTime)=="23:30:00":
                                            bmrcolor45="orange"
                                            bmrcolor46="orange"
                                            bmrcolor47="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            #bmrcolor25="orange"
                                            bmrcolor45="orange"
                                            bmrcolor46="orange"
                                            bmrcolor47="orange"
                                            bmrcolor48="orange"
                                    elif str(reservation.startTime)=="22:00:00":
                                        bmrcolor45="orange"
                                        if str(reservation.endTime)=="23:00:00":
                                            bmrcolor46="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            bmrcolor48="orange"
                                            bmrcolor46="orange"
                                            bmrcolor47="orange"
                                        if str(reservation.endTime)=="1:00:00":
                                            #bmrcolor25="orange"
                                            #bmrcolor26="orange"
                                            bmrcolor46="orange"
                                            bmrcolor47="orange"
                                            bmrcolor48="orange"
                                    elif str(reservation.startTime)=="22:30:00":
                                        bmrcolor46="orange"
                                        if str(reservation.endTime)=="23:30:00":
                                            bmrcolor47="orange"
                                        if str(reservation.endTime)=="00:30:00":
                                            bmrcolor48="orange"
                                            #bmrcolor25="orange"
                                            bmrcolor47="orange"
                                        if str(reservation.endTime)=="01:30:00":
                                            #bmrcolor25="orange"
                                            #bmrcolor26="orange"
                                            #bmrcolor27="orange"
                                            bmrcolor47="orange"
                                            bmrcolor48="orange"
                                    elif str(reservation.startTime)=="23:00:00":
                                        bmrcolor47="orange"
                                        if str(reservation.endTime)=="00:00:00":
                                            bmrcolor48="orange"
                                        if str(reservation.endTime)=="01:00:00":
                                            bmrcolor48="orange"
                                            #bmrcolor25="orange"
                                            #bmrcolor26="orange"
                                        if str(reservation.endTime)=="02:00:00":
                                            #bmrcolor25="orange"
                                            #bmrcolor26="orange"
                                            #bmrcolor27="orange"
                                            #bmrcolor28="orange"
                                            bmrcolor48="orange"
                                    elif str(reservation.startTime)=="23:30:00":
                                        bmrcolor48="orange"
                                        #if str(reservation.endTime)=="00:30:00":
                                            #bmrcolor25="orange"
                                        #elif str(reservation.endTime)=="01:30:00":
                                            #bmrcolor27="orange"
                                            #bmrcolor25="orange"
                                            #bmrcolor26="orange"
                                        #elif str(r.endTime)=="02:30:00":
                                            #bmrcolor25="orange"
                                            #trcolor26="orange"
                                            #bmrcolor27="orange"
                                            #bmrcolor28="orange"
                                            #bmrcolor29="red"
                return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,
                'smrcolor1':smrcolor1,'smrcolor2':smrcolor2,'smrcolor3':smrcolor3,'smrcolor4':smrcolor4,'smrcolor5':smrcolor5,'smrcolor6':smrcolor6,'smrcolor7':smrcolor7,
                'smrcolor8':smrcolor8,'smrcolor9':smrcolor9,'smrcolor10':smrcolor10,'smrcolor11':smrcolor11,'smrcolor12':smrcolor12,'smrcolor13':smrcolor13,
                'smrcolor14':smrcolor14,'smrcolor15':smrcolor15,'smrcolor16':smrcolor16,'smrcolor17':smrcolor17,'smrcolor18':smrcolor18,'smrcolor19':smrcolor19,
                'smrcolor20':smrcolor20,'smrcolor21':smrcolor21,'smrcolor22':smrcolor22,'smrcolor23':smrcolor23,'smrcolor24':smrcolor24,'smrcolor25':smrcolor25,
                'smrcolor26':smrcolor26,'smrcolor27':smrcolor27,'smrcolor28':smrcolor28,'smrcolor29':smrcolor29,'smrcolor30':smrcolor30,'smrcolor31':smrcolor31,
                'smrcolor32':smrcolor32,'smrcolor33':smrcolor33,'smrcolor34':smrcolor34,'smrcolor35':smrcolor35,'smrcolor36':smrcolor36,'smrcolor37':smrcolor37,
                'smrcolor38':smrcolor38,'smrcolor39':smrcolor39,'smrcolor40':smrcolor40,'smrcolor41':smrcolor41,'smrcolor42':smrcolor42,'smrcolor43':smrcolor43,
                'smrcolor44':smrcolor44,'smrcolor45':smrcolor45,'smrcolor46':smrcolor46,'smrcolor47':smrcolor47,'smrcolor48':smrcolor48,

                'trcolor1':trcolor1,'trcolor2':trcolor2,'trcolor3':trcolor3,'trcolor4':trcolor4,'trcolor5':trcolor5,'trcolor6':trcolor6,'trcolor7':trcolor7,
                'trcolor8':trcolor8,'trcolor9':trcolor9,'trcolor10':trcolor10,'trcolor11':trcolor11,'trcolor12':trcolor12,'trcolor13':trcolor13,
                'trcolor14':trcolor14,'trcolor15':trcolor15,'trcolor16':trcolor16,'trcolor17':trcolor17,'trcolor18':trcolor18,'trcolor19':trcolor19,
                'trcolor20':trcolor20,'trcolor21':trcolor21,'trcolor22':trcolor22,'trcolor23':trcolor23,'trcolor24':trcolor24,'trcolor25':trcolor25,
                'trcolor26':trcolor26,'trcolor27':trcolor27,'trcolor28':trcolor28,'trcolor29':trcolor29,'trcolor30':trcolor30,'trcolor31':trcolor31,
                'trcolor32':trcolor32,'trcolor33':trcolor33,'trcolor34':trcolor34,'trcolor35':trcolor35,'trcolor36':trcolor36,'trcolor37':trcolor37,
                'trcolor38':trcolor38,'trcolor39':trcolor39,'trcolor40':trcolor40,'trcolor41':trcolor41,'trcolor42':trcolor42,'trcolor43':trcolor43,
                'trcolor44':trcolor44,'trcolor45':trcolor45,'trcolor46':trcolor46,'trcolor47':trcolor47,'trcolor48':trcolor48,

                'bmrcolor1':bmrcolor1,'bmrcolor2':bmrcolor2,'bmrcolor3':bmrcolor3,'bmrcolor4':bmrcolor4,'bmrcolor5':bmrcolor5,'bmrcolor6':bmrcolor6,'bmrcolor7':bmrcolor7,
                'bmrcolor8':bmrcolor8,'bmrcolor9':bmrcolor9,'bmrcolor10':bmrcolor10,'bmrcolor11':bmrcolor11,'bmrcolor12':bmrcolor12,'bmrcolor13':bmrcolor13,
                'bmrcolor14':bmrcolor14,'bmrcolor15':bmrcolor15,'bmrcolor16':bmrcolor16,'bmrcolor17':bmrcolor17,'bmrcolor18':bmrcolor18,'bmrcolor19':bmrcolor19,
                'bmrcolor20':bmrcolor20,'bmrcolor21':bmrcolor21,'bmrcolor22':bmrcolor22,'bmrcolor23':bmrcolor23,'bmrcolor24':bmrcolor24,'bmrcolor25':bmrcolor25,
                'bmrcolor26':bmrcolor26,'bmrcolor27':bmrcolor27,'bmrcolor28':bmrcolor28,'bmrcolor29':bmrcolor29,'bmrcolor30':bmrcolor30,'bmrcolor31':bmrcolor31,
                'bmrcolor32':bmrcolor32,'bmrcolor33':bmrcolor33,'bmrcolor34':bmrcolor34,'bmrcolor35':bmrcolor35,'bmrcolor36':bmrcolor36,'bmrcolor37':bmrcolor37,
                'bmrcolor38':bmrcolor38,'bmrcolor39':bmrcolor39,'bmrcolor40':bmrcolor40,'bmrcolor41':bmrcolor41,'bmrcolor42':bmrcolor42,'bmrcolor43':bmrcolor43,
                'bmrcolor44':bmrcolor44,'bmrcolor45':bmrcolor45,'bmrcolor46':bmrcolor46,'bmrcolor47':bmrcolor47,'bmrcolor48':bmrcolor48,
            })
            else:
                formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(minutes=int(request.POST.get('duration')))).time())
                reservation.endTime = formend
                reservation.save()
                message = "Reservation recorded successfully !"

                if reservation.date==datetime.date.today():
                                if reservation.typeOf=="Small meeting room":
                                    if str(reservation.startTime)=="00:00:00":
                                        smrcolor1="red"
                                        if str(reservation.endTime)=="01:00:00":
                                            smrcolor2="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            smrcolor2="red"
                                            smrcolor3="red"
                                            smrcolor4="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            smrcolor2="red"
                                            smrcolor3="red"
                                            smrcolor4="red"
                                            smrcolor5="red"
                                            smrcolor6="red"
                                    elif str(reservation.startTime)=="00:30:00":
                                        smrcolor2="red"
                                        if str(reservation.endTime)=="01:30:00":
                                            smrcolor3="red"
                                        if str(reservation.endTime)=="2:30:00":
                                            smrcolor3="red"
                                            smrcolor4="red"
                                            smrcolor5="red"
                                        if str(reservation.endTime)=="3:30:00":
                                            smrcolor7="red"
                                            smrcolor3="red"
                                            smrcolor4="red"
                                            smrcolor5="red"
                                            smrcolor6="red"
                                    elif str(reservation.startTime)=="01:00:00":
                                        smrcolor3="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            smrcolor4="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            smrcolor4="red"
                                            smrcolor5="red"
                                            smrcolor6="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            smrcolor8="red"
                                            smrcolor7="red"
                                            smrcolor4="red"
                                            smrcolor5="red"
                                            smrcolor6="red"
                                    elif str(reservation.startTime)=="01:30:00":
                                        smrcolor4="red"
                                        if str(reservation.endTime)=="02:30:00":
                                            smrcolor5="red"
                                        if str(reservation.endTime)=="03:30:00":
                                            smrcolor5="red"
                                            smrcolor6="red"
                                            smrcolor7="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            smrcolor5="red"
                                            smrcolor6="red"
                                            smrcolor7="red"
                                            smrcolor8="red"
                                            smrcolor9="red"
                                    elif str(reservation.startTime)=="02:00:00":
                                        smrcolor5="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            smrcolor6="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            smrcolor6="red"
                                            smrcolor7="red"
                                            smrcolor8="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            smrcolor10="red"
                                            smrcolor6="red"
                                            smrcolor7="red"
                                            smrcolor8="red"
                                            smrcolor9="red"
                                    elif str(reservation.startTime)=="02:30:00":
                                        smrcolor6="red"
                                        if str(reservation.endTime)=="03:30:00":
                                            smrcolor7="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            smrcolor9="red"
                                            smrcolor7="red"
                                            smrcolor8="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            smrcolor10="red"
                                            smrcolor11="red"
                                            smrcolor7="red"
                                            smrcolor8="red"
                                            smrcolor9="red"
                                    elif str(reservation.startTime)=="03:00:00":
                                        smrcolor7="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            smrcolor8="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            smrcolor9="red"
                                            smrcolor10="red"
                                            smrcolor8="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor10="red"
                                            smrcolor11="red"
                                            smrcolor12="red"
                                            smrcolor8="red"
                                            smrcolor9="red"
                                    elif str(reservation.startTime)=="03:30:00":
                                        smrcolor8="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            smrcolor9="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            smrcolor9="red"
                                            smrcolor10="red"
                                            smrcolor11="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            smrcolor10="red"
                                            smrcolor11="red"
                                            smrcolor12="red"
                                            smrcolor13="red"
                                            smrcolor9="red"
                                    elif str(reservation.startTime)=="04:00:00":
                                        smrcolor9="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            smrcolor10="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor12="red"
                                            smrcolor10="red"
                                            smrcolor11="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            smrcolor10="red"
                                            smrcolor11="red"
                                            smrcolor12="red"
                                            smrcolor13="red"
                                            smrcolor14="red"
                                    elif str(reservation.startTime)=="04:30:00":
                                        smrcolor10="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            smrcolor11="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            smrcolor12="red"
                                            smrcolor13="red"
                                            smrcolor11="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            smrcolor15="red"
                                            smrcolor11="red"
                                            smrcolor12="red"
                                            smrcolor13="red"
                                            smrcolor14="red"
                                    elif str(reservation.startTime)=="05:00:00":
                                        smrcolor11="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor12="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            smrcolor12="red"
                                            smrcolor13="red"
                                            smrcolor14="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            smrcolor15="red"
                                            smrcolor16="red"
                                            smrcolor12="red"
                                            smrcolor13="red"
                                            smrcolor14="red"
                                    elif str(reservation.startTime)=="05:30:00":
                                        smrcolor12="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            smrcolor13="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            smrcolor15="red"
                                            smrcolor13="red"
                                            smrcolor14="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            smrcolor15="red"
                                            smrcolor16="red"
                                            smrcolor17="red"
                                            smrcolor13="red"
                                            smrcolor14="red"
                                    elif str(reservation.startTime)=="06:00:00":
                                        smrcolor13="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            smrcolor14="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            smrcolor15="red"
                                            smrcolor16="red"
                                            smrcolor14="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor15="red"
                                            smrcolor16="red"
                                            smrcolor17="red"
                                            smrcolor18="red"
                                            smrcolor14="red"
                                    elif str(reservation.startTime)=="06:30:00":
                                        smrcolor14="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            smrcolor15="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            smrcolor15="red"
                                            smrcolor16="red"
                                            smrcolor17="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor15="red"
                                            smrcolor16="red"
                                            smrcolor17="red"
                                            smrcolor18="red"
                                            smrcolor19="red"
                                    elif str(reservation.startTime)=="07:00:00":
                                        smrcolor15="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            smrcolor16="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor18="red"
                                            smrcolor16="red"
                                            smrcolor17="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor20="red"
                                            smrcolor16="red"
                                            smrcolor17="red"
                                            smrcolor18="red"
                                            smrcolor19="red"
                                    elif str(reservation.startTime)=="07:30:00":
                                        smrcolor16="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            smrcolor17="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor18="red"
                                            smrcolor19="red"
                                            smrcolor17="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor20="red"
                                            smrcolor21="red"
                                            smrcolor17="red"
                                            smrcolor18="red"
                                            smrcolor19="red"
                                    elif str(reservation.startTime)=="08:00:00":
                                        smrcolor17="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor18="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor18="red"
                                            smrcolor19="red"
                                            smrcolor20="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor20="red"
                                            smrcolor21="red"
                                            smrcolor22="red"
                                            smrcolor18="red"
                                            smrcolor19="red"
                                    elif str(reservation.startTime)=="08:30:00":
                                        smrcolor18="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor19="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor21="red"
                                            smrcolor19="red"
                                            smrcolor20="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            smrcolor20="red"
                                            smrcolor21="red"
                                            smrcolor22="red"
                                            smrcolor23="red"
                                            smrcolor19="red"
                                    elif str(reservation.startTime)=="09:00:00":
                                        smrcolor19="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor20="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor21="red"
                                            smrcolor22="red"
                                            smrcolor20="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor20="red"
                                            smrcolor21="red"
                                            smrcolor22="red"
                                            smrcolor23="red"
                                            smrcolor24="red"
                                    elif str(reservation.startTime)=="09:30:00":
                                        smrcolor20="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor21="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            smrcolor21="red"
                                            smrcolor22="red"
                                            smrcolor23="red"
                                        if str(reservation.endTime)=="12:30:00":
                                            smrcolor25="red"
                                            smrcolor21="red"
                                            smrcolor22="red"
                                            smrcolor23="red"
                                            smrcolor24="red"
                                    elif str(reservation.startTime)=="10:00:00":
                                        smrcolor21="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor22="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor24="red"
                                            smrcolor22="red"
                                            smrcolor23="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor25="red"
                                            smrcolor26="red"
                                            smrcolor22="red"
                                            smrcolor23="red"
                                            smrcolor24="red"
                                    elif str(reservation.startTime)=="10:30:00":
                                        smrcolor22="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor23="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor24="red"
                                            smrcolor25="red"
                                            smrcolor23="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor25="red"
                                            smrcolor26="red"
                                            smrcolor27="red"
                                            smrcolor23="red"
                                            smrcolor24="red"
                                    elif str(reservation.startTime)=="11:00:00":
                                        smrcolor23="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor24="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            smrcolor24="red"
                                            smrcolor25="red"
                                            smrcolor26="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor25="red"
                                            smrcolor26="red"
                                            smrcolor27="red"
                                            smrcolor28="red"
                                            smrcolor24="red"
                                    elif str(reservation.startTime)=="11:30:00":
                                        smrcolor24="red"
                                        if str(reservation.endTime)=="12:30:00":
                                            smrcolor25="red"
                                        if str(reservation.endTime)=="13:30:00":
                                            smrcolor27="red"
                                            smrcolor25="red"
                                            smrcolor26="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            smrcolor25="red"
                                            smrcolor26="red"
                                            smrcolor27="red"
                                            smrcolor28="red"
                                            smrcolor29="red"




                                    elif str(reservation.startTime)=="12:00:00":
                                        smrcolor25="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            smrcolor26="red"
                                        if str(reservation.endTime)=="14:00:00":
                                            smrcolor26="red"
                                            smrcolor27="red"
                                            smrcolor28="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            smrcolor26="red"
                                            smrcolor27="red"
                                            smrcolor28="red"
                                            smrcolor29="red"
                                            smrcolor30="red"
                                    elif str(reservation.startTime)=="12:30:00":
                                        smrcolor2="red"
                                        if str(reservation.endTime)=="13:30:00":
                                            smrcolor27="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            smrcolor27="red"
                                            smrcolor28="red"
                                            smrcolor29="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            smrcolor31="red"
                                            smrcolor27="red"
                                            smrcolor28="red"
                                            smrcolor29="red"
                                            smrcolor30="red"
                                    elif str(reservation.startTime)=="13:00:00":
                                        smrcolor27="red"
                                        if str(reservation.endTime)=="14:00:00":
                                            smrcolor28="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            smrcolor28="red"
                                            smrcolor29="red"
                                            smrcolor30="red"
                                        if str(reservation.endTime)=="16:00:00":
                                            smrcolor32="red"
                                            smrcolor31="red"
                                            smrcolor28="red"
                                            smrcolor29="red"
                                            smrcolor30="red"
                                    elif str(reservation.startTime)=="13:30:00":
                                        smrcolor28="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            smrcolor29="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            smrcolor29="red"
                                            smrcolor30="red"
                                            smrcolor31="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            smrcolor29="red"
                                            smrcolor30="red"
                                            smrcolor31="red"
                                            smrcolor32="red"
                                            smrcolor33="red"
                                    elif str(reservation.startTime)=="14:00:00":
                                        smrcolor29="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            smrcolor30="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            smrcolor30="red"
                                            smrcolor31="red"
                                            smrcolor32="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            smrcolor34="red"
                                            smrcolor30="red"
                                            smrcolor31="red"
                                            smrcolor32="red"
                                            smrcolor33="red"
                                    elif str(reservation.startTime)=="14:30:00":
                                        smrcolor30="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            smrcolor31="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            smrcolor33="red"
                                            smrcolor31="red"
                                            smrcolor32="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            smrcolor34="red"
                                            smrcolor35="red"
                                            smrcolor31="red"
                                            smrcolor32="red"
                                            smrcolor33="red"
                                    elif str(reservation.startTime)=="15:00:00":
                                        smrcolor31="red"
                                        if str(reservation.endTime)=="16:00:00":
                                            smrcolor32="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            smrcolor33="red"
                                            smrcolor34="red"
                                            smrcolor32="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            smrcolor34="red"
                                            smrcolor35="red"
                                            smrcolor12="red"
                                            smrcolor32="red"
                                            smrcolor33="red"
                                    elif str(reservation.startTime)=="15:30:00":
                                        smrcolor32="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            smrcolor33="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            smrcolor33="red"
                                            smrcolor34="red"
                                            smrcolor35="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            smrcolor34="red"
                                            smrcolor35="red"
                                            smrcolor36="red"
                                            smrcolor37="red"
                                            smrcolor33="red"
                                    elif str(reservation.startTime)=="16:00:00":
                                        smrcolor33="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            smrcolor34="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            smrcolor36="red"
                                            smrcolor34="red"
                                            smrcolor35="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            smrcolor34="red"
                                            smrcolor35="red"
                                            smrcolor36="red"
                                            smrcolor37="red"
                                            smrcolor38="red"
                                    elif str(reservation.startTime)=="16:30:00":
                                        smrcolor34="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            smrcolor35="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            smrcolor36="red"
                                            smrcolor37="red"
                                            smrcolor35="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            smrcolor39="red"
                                            smrcolor35="red"
                                            smrcolor36="red"
                                            smrcolor37="red"
                                            smrcolor38="red"
                                    elif str(reservation.startTime)=="17:00:00":
                                        smrcolor35="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            smrcolor36="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            smrcolor36="red"
                                            smrcolor37="red"
                                            smrcolor38="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            smrcolor39="red"
                                            smrcolor40="red"
                                            smrcolor36="red"
                                            smrcolor37="red"
                                            smrcolor38="red"
                                    elif str(reservation.startTime)=="17:30:00":
                                        smrcolor36="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            smrcolor37="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            smrcolor39="red"
                                            smrcolor37="red"
                                            smrcolor38="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            smrcolor39="red"
                                            smrcolor40="red"
                                            smrcolor41="red"
                                            smrcolor37="red"
                                            smrcolor38="red"
                                    elif str(reservation.startTime)=="18:00:00":
                                        smrcolor37="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            smrcolor38="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            smrcolor39="red"
                                            smrcolor40="red"
                                            smrcolor38="red"
                                        if str(reservation.endTime)=="21:00:00":
                                            smrcolor39="red"
                                            smrcolor40="red"
                                            smrcolor41="red"
                                            smrcolor42="red"
                                            smrcolor38="red"
                                    elif str(reservation.startTime)=="18:30:00":
                                        smrcolor38="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            smrcolor39="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            smrcolor39="red"
                                            smrcolor40="red"
                                            smrcolor41="red"
                                        if str(reservation.endTime)=="21:30:00":
                                            smrcolor39="red"
                                            smrcolor40="red"
                                            smrcolor41="red"
                                            smrcolor42="red"
                                            smrcolor43="red"
                                    elif str(reservation.startTime)=="19:00:00":
                                        smrcolor39="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            smrcolor40="red"
                                        if str(reservation.endTime)=="21:00:00":
                                            smrcolor42="red"
                                            smrcolor40="red"
                                            smrcolor41="red"
                                        if str(reservation.endTime)=="22:00:00":
                                            smrcolor44="red"
                                            smrcolor40="red"
                                            smrcolor41="red"
                                            smrcolor42="red"
                                            smrcolor43="red"
                                    elif str(reservation.startTime)=="19:30:00":
                                        smrcolor40="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            smrcolor41="red"
                                        if str(reservation.endTime)=="21:30:00":
                                            smrcolor42="red"
                                            smrcolor43="red"
                                            smrcolor41="red"
                                        if str(reservation.endTime)=="22:30:00":
                                            smrcolor44="red"
                                            smrcolor45="red"
                                            smrcolor41="red"
                                            smrcolor42="red"
                                            smrcolor43="red"
                                    elif str(reservation.startTime)=="08:00:00":
                                        smrcolor41="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            smrcolor42="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            smrcolor42="red"
                                            smrcolor43="red"
                                            smrcolor44="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            smrcolor44="red"
                                            smrcolor45="red"
                                            smrcolor46="red"
                                            smrcolor42="red"
                                            smrcolor43="red"
                                    elif str(reservation.startTime)=="08:30:00":
                                        smrcolor42="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            smrcolor43="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            smrcolor45="red"
                                            smrcolor43="red"
                                            smrcolor44="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            smrcolor44="red"
                                            smrcolor45="red"
                                            smrcolor46="red"
                                            smrcolor47="red"
                                            smrcolor43="red"
                                    elif str(reservation.startTime)=="21:00:00":
                                        smrcolor43="red"
                                        if str(reservation.endTime)=="22:00:00":
                                            smrcolor44="red"
                                        if str(reservation.endTime)=="23:00:00":
                                            smrcolor45="red"
                                            smrcolor46="red"
                                            smrcolor44="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            smrcolor44="red"
                                            smrcolor45="red"
                                            smrcolor46="red"
                                            smrcolor47="red"
                                            smrcolor48="red"
                                    elif str(reservation.startTime)=="21:30:00":
                                        smrcolor44="red"
                                        if str(reservation.endTime)=="22:30:00":
                                            smrcolor45="red"
                                        if str(reservation.endTime)=="23:30:00":
                                            smrcolor45="red"
                                            smrcolor46="red"
                                            smrcolor47="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            #smrcolor25="red"
                                            smrcolor45="red"
                                            smrcolor46="red"
                                            smrcolor47="red"
                                            smrcolor48="red"
                                    elif str(reservation.startTime)=="22:00:00":
                                        smrcolor45="red"
                                        if str(reservation.endTime)=="23:00:00":
                                            smrcolor46="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            smrcolor48="red"
                                            smrcolor46="red"
                                            smrcolor47="red"
                                        if str(reservation.endTime)=="1:00:00":
                                            #smrcolor25="red"
                                            #smrcolor26="red"
                                            smrcolor46="red"
                                            smrcolor47="red"
                                            smrcolor48="red"
                                    elif str(reservation.startTime)=="22:30:00":
                                        smrcolor46="red"
                                        if str(reservation.endTime)=="23:30:00":
                                            smrcolor47="red"
                                        if str(reservation.endTime)=="00:30:00":
                                            smrcolor48="red"
                                            #smrcolor25="red"
                                            smrcolor47="red"
                                        if str(reservation.endTime)=="01:30:00":
                                            #smrcolor25="red"
                                            #smrcolor26="red"
                                            #smrcolor27="red"
                                            smrcolor47="red"
                                            smrcolor48="red"
                                    elif str(reservation.startTime)=="23:00:00":
                                        smrcolor47="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            smrcolor48="red"
                                        if str(reservation.endTime)=="01:00:00":
                                            smrcolor48="red"
                                            #smrcolor25="red"
                                            #smrcolor26="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            #smrcolor25="red"
                                            #smrcolor26="red"
                                            #smrcolor27="red"
                                            #smrcolor28="red"
                                            smrcolor48="red"
                                    elif str(reservation.startTime)=="23:30:00":
                                        smrcolor48="red"
                                        #if str(reservation.endTime)=="00:30:00":
                                            #smrcolor25="red"
                                        #elif str(reservation.endTime)=="01:30:00":
                                            #smrcolor27="red"
                                            #smrcolor25="red"
                                            #smrcolor26="red"
                                        #elif str(reservation.endTime)=="02:30:00":
                                            #smrcolor25="red"
                                            #smrcolor26="red"
                                            #smrcolor27="red"
                                            #smrcolor28="red"
                                            #smrcolor29="red"
                                elif reservation.typeOf=="Training Room":
                                    if str(reservation.startTime)=="00:00:00":
                                        trcolor1="red"
                                        if str(reservation.endTime)=="01:00:00":
                                            trcolor2="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            trcolor2="red"
                                            trcolor3="red"
                                            trcolor4="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            trcolor2="red"
                                            trcolor3="red"
                                            trcolor4="red"
                                            trcolor5="red"
                                            trcolor6="red"
                                    elif str(reservation.startTime)=="00:30:00":
                                        trcolor2="red"
                                        if str(reservation.endTime)=="01:30:00":
                                            trcolor3="red"
                                        if str(reservation.endTime)=="2:30:00":
                                            trcolor3="red"
                                            trcolor4="red"
                                            trcolor5="red"
                                        if str(reservation.endTime)=="3:30:00":
                                            trcolor7="red"
                                            trcolor3="red"
                                            trcolor4="red"
                                            trcolor5="red"
                                            trcolor6="red"
                                    elif str(reservation.startTime)=="01:00:00":
                                        trcolor3="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            trcolor4="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            trcolor4="red"
                                            trcolor5="red"
                                            trcolor6="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            trcolor8="red"
                                            trcolor7="red"
                                            trcolor4="red"
                                            trcolor5="red"
                                            trcolor6="red"
                                    elif str(reservation.startTime)=="01:30:00":
                                        trcolor4="red"
                                        if str(reservation.endTime)=="02:30:00":
                                            trcolor5="red"
                                        if str(reservation.endTime)=="03:30:00":
                                            trcolor5="red"
                                            trcolor6="red"
                                            trcolor7="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            trcolor5="red"
                                            trcolor6="red"
                                            trcolor7="red"
                                            trcolor8="red"
                                            trcolor9="red"
                                    elif str(reservation.startTime)=="02:00:00":
                                        trcolor5="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            trcolor6="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            trcolor6="red"
                                            trcolor7="red"
                                            trcolor8="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            trcolor10="red"
                                            trcolor6="red"
                                            trcolor7="red"
                                            trcolor8="red"
                                            trcolor9="red"
                                    elif str(reservation.startTime)=="02:30:00":
                                        trcolor6="red"
                                        if str(reservation.endTime)=="03:30:00":
                                            trcolor7="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            trcolor9="red"
                                            trcolor7="red"
                                            trcolor8="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            trcolor10="red"
                                            trcolor11="red"
                                            trcolor7="red"
                                            trcolor8="red"
                                            trcolor9="red"
                                    elif str(reservation.startTime)=="03:00:00":
                                        trcolor7="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            trcolor8="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            trcolor9="red"
                                            trcolor10="red"
                                            trcolor8="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor10="red"
                                            trcolor11="red"
                                            trcolor12="red"
                                            trcolor8="red"
                                            trcolor9="red"
                                    elif str(reservation.startTime)=="03:30:00":
                                        trcolor8="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            trcolor9="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            trcolor9="red"
                                            trcolor10="red"
                                            trcolor11="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            trcolor10="red"
                                            trcolor11="red"
                                            trcolor12="red"
                                            trcolor13="red"
                                            trcolor9="red"
                                    elif str(reservation.startTime)=="04:00:00":
                                        trcolor9="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            trcolor10="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor12="red"
                                            trcolor10="red"
                                            trcolor11="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            trcolor10="red"
                                            trcolor11="red"
                                            trcolor12="red"
                                            trcolor13="red"
                                            trcolor14="red"
                                    elif str(reservation.startTime)=="04:30:00":
                                        trcolor10="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            trcolor11="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            trcolor12="red"
                                            trcolor13="red"
                                            trcolor11="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            trcolor15="red"
                                            trcolor11="red"
                                            trcolor12="red"
                                            trcolor13="red"
                                            trcolor14="red"
                                    elif str(reservation.startTime)=="05:00:00":
                                        trcolor11="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor12="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            trcolor12="red"
                                            trcolor13="red"
                                            trcolor14="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            trcolor15="red"
                                            trcolor16="red"
                                            trcolor12="red"
                                            trcolor13="red"
                                            trcolor14="red"
                                    elif str(reservation.startTime)=="05:30:00":
                                        trcolor12="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            trcolor13="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            trcolor15="red"
                                            trcolor13="red"
                                            trcolor14="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            trcolor15="red"
                                            trcolor16="red"
                                            trcolor17="red"
                                            trcolor13="red"
                                            trcolor14="red"
                                    elif str(reservation.startTime)=="06:00:00":
                                        trcolor13="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            trcolor14="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            trcolor15="red"
                                            trcolor16="red"
                                            trcolor14="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor15="red"
                                            trcolor16="red"
                                            trcolor17="red"
                                            trcolor18="red"
                                            trcolor14="red"
                                    elif str(reservation.startTime)=="06:30:00":
                                        trcolor14="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            trcolor15="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            trcolor15="red"
                                            trcolor16="red"
                                            trcolor17="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor15="red"
                                            trcolor16="red"
                                            trcolor17="red"
                                            trcolor18="red"
                                            trcolor19="red"
                                    elif str(reservation.startTime)=="07:00:00":
                                        trcolor15="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            trcolor16="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor18="red"
                                            trcolor16="red"
                                            trcolor17="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor20="red"
                                            trcolor16="red"
                                            trcolor17="red"
                                            trcolor18="red"
                                            trcolor19="red"
                                    elif str(reservation.startTime)=="07:30:00":
                                        trcolor16="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            trcolor17="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor18="red"
                                            trcolor19="red"
                                            trcolor17="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor20="red"
                                            trcolor21="red"
                                            trcolor17="red"
                                            trcolor18="red"
                                            trcolor19="red"
                                    elif str(reservation.startTime)=="08:00:00":
                                        trcolor17="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor18="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor18="red"
                                            trcolor19="red"
                                            trcolor20="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor20="red"
                                            trcolor21="red"
                                            trcolor22="red"
                                            trcolor18="red"
                                            trcolor19="red"
                                    elif str(reservation.startTime)=="08:30:00":
                                        trcolor18="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor19="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor21="red"
                                            trcolor19="red"
                                            trcolor20="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            trcolor20="red"
                                            trcolor21="red"
                                            trcolor22="red"
                                            trcolor23="red"
                                            trcolor19="red"
                                    elif str(reservation.startTime)=="09:00:00":
                                        trcolor19="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor20="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor21="red"
                                            trcolor22="red"
                                            trcolor20="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor20="red"
                                            trcolor21="red"
                                            trcolor22="red"
                                            trcolor23="red"
                                            trcolor24="red"
                                    elif str(reservation.startTime)=="09:30:00":
                                        trcolor20="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor21="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            trcolor21="red"
                                            trcolor22="red"
                                            trcolor23="red"
                                        if str(reservation.endTime)=="12:30:00":
                                            trcolor25="red"
                                            trcolor21="red"
                                            trcolor22="red"
                                            trcolor23="red"
                                            trcolor24="red"
                                    elif str(reservation.startTime)=="10:00:00":
                                        trcolor21="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor22="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor24="red"
                                            trcolor22="red"
                                            trcolor23="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor25="red"
                                            trcolor26="red"
                                            trcolor22="red"
                                            trcolor23="red"
                                            trcolor24="red"
                                    elif str(reservation.startTime)=="10:30:00":
                                        trcolor22="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor23="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor24="red"
                                            trcolor25="red"
                                            trcolor23="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor25="red"
                                            trcolor26="red"
                                            trcolor27="red"
                                            trcolor23="red"
                                            trcolor24="red"
                                    elif str(reservation.startTime)=="11:00:00":
                                        trcolor23="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor24="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            trcolor24="red"
                                            trcolor25="red"
                                            trcolor26="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor25="red"
                                            trcolor26="red"
                                            trcolor27="red"
                                            trcolor28="red"
                                            trcolor24="red"
                                    elif str(reservation.startTime)=="11:30:00":
                                        trcolor24="red"
                                        if str(reservation.endTime)=="12:30:00":
                                            trcolor25="red"
                                        if str(reservation.endTime)=="13:30:00":
                                            trcolor27="red"
                                            trcolor25="red"
                                            trcolor26="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            trcolor25="red"
                                            trcolor26="red"
                                            trcolor27="red"
                                            trcolor28="red"
                                            trcolor29="red"




                                    elif str(reservation.startTime)=="12:00:00":
                                        trcolor25="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            trcolor26="red"
                                        if str(reservation.endTime)=="14:00:00":
                                            trcolor26="red"
                                            trcolor27="red"
                                            trcolor28="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            trcolor26="red"
                                            trcolor27="red"
                                            trcolor28="red"
                                            trcolor29="red"
                                            trcolor30="red"
                                    elif str(reservation.startTime)=="12:30:00":
                                        trcolor2="red"
                                        if str(reservation.endTime)=="13:30:00":
                                            trcolor27="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            trcolor27="red"
                                            trcolor28="red"
                                            trcolor29="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            trcolor31="red"
                                            trcolor27="red"
                                            trcolor28="red"
                                            trcolor29="red"
                                            trcolor30="red"
                                    elif str(reservation.startTime)=="13:00:00":
                                        trcolor27="red"
                                        if str(reservation.endTime)=="14:00:00":
                                            trcolor28="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            trcolor28="red"
                                            trcolor29="red"
                                            trcolor30="red"
                                        if str(reservation.endTime)=="16:00:00":
                                            trcolor32="red"
                                            trcolor31="red"
                                            trcolor28="red"
                                            trcolor29="red"
                                            trcolor30="red"
                                    elif str(reservation.startTime)=="13:30:00":
                                        trcolor28="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            trcolor29="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            trcolor29="red"
                                            trcolor30="red"
                                            trcolor31="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            trcolor29="red"
                                            trcolor30="red"
                                            trcolor31="red"
                                            trcolor32="red"
                                            trcolor33="red"
                                    elif str(reservation.startTime)=="14:00:00":
                                        trcolor29="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            trcolor30="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            trcolor30="red"
                                            trcolor31="red"
                                            trcolor32="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            trcolor34="red"
                                            trcolor30="red"
                                            trcolor31="red"
                                            trcolor32="red"
                                            trcolor33="red"
                                    elif str(reservation.startTime)=="14:30:00":
                                        trcolor30="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            trcolor31="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            trcolor33="red"
                                            trcolor31="red"
                                            trcolor32="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            trcolor34="red"
                                            trcolor35="red"
                                            trcolor31="red"
                                            trcolor32="red"
                                            trcolor33="red"
                                    elif str(reservation.startTime)=="15:00:00":
                                        trcolor31="red"
                                        if str(reservation.endTime)=="16:00:00":
                                            trcolor32="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            trcolor33="red"
                                            trcolor34="red"
                                            trcolor32="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            trcolor34="red"
                                            trcolor35="red"
                                            trcolor12="red"
                                            trcolor32="red"
                                            trcolor33="red"
                                    elif str(reservation.startTime)=="15:30:00":
                                        trcolor32="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            trcolor33="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            trcolor33="red"
                                            trcolor34="red"
                                            trcolor35="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            trcolor34="red"
                                            trcolor35="red"
                                            trcolor36="red"
                                            trcolor37="red"
                                            trcolor33="red"
                                    elif str(reservation.startTime)=="16:00:00":
                                        trcolor33="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            trcolor34="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            trcolor36="red"
                                            trcolor34="red"
                                            trcolor35="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            trcolor34="red"
                                            trcolor35="red"
                                            trcolor36="red"
                                            trcolor37="red"
                                            trcolor38="red"
                                    elif str(reservation.startTime)=="16:30:00":
                                        trcolor34="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            trcolor35="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            trcolor36="red"
                                            trcolor37="red"
                                            trcolor35="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            trcolor39="red"
                                            trcolor35="red"
                                            trcolor36="red"
                                            trcolor37="red"
                                            trcolor38="red"
                                    elif str(reservation.startTime)=="17:00:00":
                                        trcolor35="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            trcolor36="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            trcolor36="red"
                                            trcolor37="red"
                                            trcolor38="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            trcolor39="red"
                                            trcolor40="red"
                                            trcolor36="red"
                                            trcolor37="red"
                                            trcolor38="red"
                                    elif str(reservation.startTime)=="17:30:00":
                                        trcolor36="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            trcolor37="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            trcolor39="red"
                                            trcolor37="red"
                                            trcolor38="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            trcolor39="red"
                                            trcolor40="red"
                                            trcolor41="red"
                                            trcolor37="red"
                                            trcolor38="red"
                                    elif str(reservation.startTime)=="18:00:00":
                                        trcolor37="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            trcolor38="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            trcolor39="red"
                                            trcolor40="red"
                                            trcolor38="red"
                                        if str(reservation.endTime)=="21:00:00":
                                            trcolor39="red"
                                            trcolor40="red"
                                            trcolor41="red"
                                            trcolor42="red"
                                            trcolor38="red"
                                    elif str(reservation.startTime)=="18:30:00":
                                        trcolor38="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            trcolor39="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            trcolor39="red"
                                            trcolor40="red"
                                            trcolor41="red"
                                        if str(reservation.endTime)=="21:30:00":
                                            trcolor39="red"
                                            trcolor40="red"
                                            trcolor41="red"
                                            trcolor42="red"
                                            trcolor43="red"
                                    elif str(reservation.startTime)=="19:00:00":
                                        trcolor39="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            trcolor40="red"
                                        if str(reservation.endTime)=="21:00:00":
                                            trcolor42="red"
                                            trcolor40="red"
                                            trcolor41="red"
                                        if str(reservation.endTime)=="22:00:00":
                                            trcolor44="red"
                                            trcolor40="red"
                                            trcolor41="red"
                                            trcolor42="red"
                                            trcolor43="red"
                                    elif str(reservation.startTime)=="19:30:00":
                                        trcolor40="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            trcolor41="red"
                                        if str(reservation.endTime)=="21:30:00":
                                            trcolor42="red"
                                            trcolor43="red"
                                            trcolor41="red"
                                        if str(reservation.endTime)=="22:30:00":
                                            trcolor44="red"
                                            trcolor45="red"
                                            trcolor41="red"
                                            trcolor42="red"
                                            trcolor43="red"
                                    elif str(reservation.startTime)=="08:00:00":
                                        trcolor41="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            trcolor42="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            trcolor42="red"
                                            trcolor43="red"
                                            trcolor44="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            trcolor44="red"
                                            trcolor45="red"
                                            trcolor46="red"
                                            trcolor42="red"
                                            trcolor43="red"
                                    elif str(reservation.startTime)=="08:30:00":
                                        trcolor42="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            trcolor43="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            trcolor45="red"
                                            trcolor43="red"
                                            trcolor44="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            trcolor44="red"
                                            trcolor45="red"
                                            trcolor46="red"
                                            trcolor47="red"
                                            trcolor43="red"
                                    elif str(reservation.startTime)=="21:00:00":
                                        trcolor43="red"
                                        if str(reservation.endTime)=="22:00:00":
                                            trcolor44="red"
                                        if str(reservation.endTime)=="23:00:00":
                                            trcolor45="red"
                                            trcolor46="red"
                                            trcolor44="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            trcolor44="red"
                                            trcolor45="red"
                                            trcolor46="red"
                                            trcolor47="red"
                                            trcolor48="red"
                                    elif str(reservation.startTime)=="21:30:00":
                                        trcolor44="red"
                                        if str(reservation.endTime)=="22:30:00":
                                            trcolor45="red"
                                        if str(reservation.endTime)=="23:30:00":
                                            trcolor45="red"
                                            trcolor46="red"
                                            trcolor47="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            #trcolor25="red"
                                            trcolor45="red"
                                            trcolor46="red"
                                            trcolor47="red"
                                            trcolor48="red"
                                    elif str(reservation.startTime)=="22:00:00":
                                        trcolor45="red"
                                        if str(reservation.endTime)=="23:00:00":
                                            trcolor46="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            trcolor48="red"
                                            trcolor46="red"
                                            trcolor47="red"
                                        if str(reservation.endTime)=="1:00:00":
                                            #trcolor25="red"
                                            #trcolor26="red"
                                            trcolor46="red"
                                            trcolor47="red"
                                            trcolor48="red"
                                    elif str(reservation.startTime)=="22:30:00":
                                        trcolor46="red"
                                        if str(reservation.endTime)=="23:30:00":
                                            trcolor47="red"
                                        if str(reservation.endTime)=="00:30:00":
                                            trcolor48="red"
                                            #trcolor25="red"
                                            trcolor47="red"
                                        if str(reservation.endTime)=="01:30:00":
                                            #trcolor25="red"
                                            #trcolor26="red"
                                            #trcolor27="red"
                                            trcolor47="red"
                                            trcolor48="red"
                                    elif str(reservation.startTime)=="23:00:00":
                                        trcolor47="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            trcolor48="red"
                                        if str(reservation.endTime)=="01:00:00":
                                            trcolor48="red"
                                            #trcolor25="red"
                                            #trcolor26="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            #trcolor25="red"
                                            #trcolor26="red"
                                            #trcolor27="red"
                                            #trcolor28="red"
                                            trcolor48="red"
                                    elif str(reservation.startTime)=="23:30:00":
                                        trcolor48="red"
                                        #if str(reservation.endTime)=="00:30:00":
                                            #trcolor25="red"
                                        #elif str(reservation.endTime)=="01:30:00":
                                            #trcolor27="red"
                                            #trcolor25="red"
                                            #trcolor26="red"
                                        #elif str(reservation.endTime)=="02:30:00":
                                            #trcolor25="red"
                                            #trcolor26="red"
                                            #trcolor27="red"
                                            #trcolor28="red"
                                            #trcolor29="red"
                                elif reservation.typeOf=="Big meeting room":
                                    if str(reservation.startTime)=="00:00:00":
                                        bmrcolor1="red"
                                        if str(reservation.endTime)=="01:00:00":
                                            bmrcolor2="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            bmrcolor2="red"
                                            bmrcolor3="red"
                                            bmrcolor4="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            bmrcolor2="red"
                                            bmrcolor3="red"
                                            bmrcolor4="red"
                                            bmrcolor5="red"
                                            bmrcolor6="red"
                                    elif str(reservation.startTime)=="00:30:00":
                                        bmrcolor2="red"
                                        if str(reservation.endTime)=="01:30:00":
                                            bmrcolor3="red"
                                        if str(reservation.endTime)=="2:30:00":
                                            bmrcolor3="red"
                                            bmrcolor4="red"
                                            bmrcolor5="red"
                                        if str(reservation.endTime)=="3:30:00":
                                            bmrcolor7="red"
                                            bmrcolor3="red"
                                            bmrcolor4="red"
                                            bmrcolor5="red"
                                            bmrcolor6="red"
                                    elif str(reservation.startTime)=="01:00:00":
                                        bmrcolor3="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            bmrcolor4="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            bmrcolor4="red"
                                            bmrcolor5="red"
                                            bmrcolor6="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            bmrcolor8="red"
                                            bmrcolor7="red"
                                            bmrcolor4="red"
                                            bmrcolor5="red"
                                            bmrcolor6="red"
                                    elif str(reservation.startTime)=="01:30:00":
                                        bmrcolor4="red"
                                        if str(reservation.endTime)=="02:30:00":
                                            bmrcolor5="red"
                                        if str(reservation.endTime)=="03:30:00":
                                            bmrcolor5="red"
                                            bmrcolor6="red"
                                            bmrcolor7="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            bmrcolor5="red"
                                            bmrcolor6="red"
                                            bmrcolor7="red"
                                            bmrcolor8="red"
                                            bmrcolor9="red"
                                    elif str(reservation.startTime)=="02:00:00":
                                        bmrcolor5="red"
                                        if str(reservation.endTime)=="03:00:00":
                                            bmrcolor6="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            bmrcolor6="red"
                                            bmrcolor7="red"
                                            bmrcolor8="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            bmrcolor10="red"
                                            bmrcolor6="red"
                                            bmrcolor7="red"
                                            bmrcolor8="red"
                                            bmrcolor9="red"
                                    elif str(reservation.startTime)=="02:30:00":
                                        bmrcolor6="red"
                                        if str(reservation.endTime)=="03:30:00":
                                            bmrcolor7="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            bmrcolor9="red"
                                            bmrcolor7="red"
                                            bmrcolor8="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            bmrcolor10="red"
                                            bmrcolor11="red"
                                            bmrcolor7="red"
                                            bmrcolor8="red"
                                            bmrcolor9="red"
                                    elif str(reservation.startTime)=="03:00:00":
                                        bmrcolor7="red"
                                        if str(reservation.endTime)=="04:00:00":
                                            bmrcolor8="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            bmrcolor9="red"
                                            bmrcolor10="red"
                                            bmrcolor8="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor10="red"
                                            bmrcolor11="red"
                                            bmrcolor12="red"
                                            bmrcolor8="red"
                                            bmrcolor9="red"
                                    elif str(reservation.startTime)=="03:30:00":
                                        bmrcolor8="red"
                                        if str(reservation.endTime)=="04:30:00":
                                            bmrcolor9="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            bmrcolor9="red"
                                            bmrcolor10="red"
                                            bmrcolor11="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            bmrcolor10="red"
                                            bmrcolor11="red"
                                            bmrcolor12="red"
                                            bmrcolor13="red"
                                            bmrcolor9="red"
                                    elif str(reservation.startTime)=="04:00:00":
                                        bmrcolor9="red"
                                        if str(reservation.endTime)=="05:00:00":
                                            bmrcolor10="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor12="red"
                                            bmrcolor10="red"
                                            bmrcolor11="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            bmrcolor10="red"
                                            bmrcolor11="red"
                                            bmrcolor12="red"
                                            bmrcolor13="red"
                                            bmrcolor14="red"
                                    elif str(reservation.startTime)=="04:30:00":
                                        bmrcolor10="red"
                                        if str(reservation.endTime)=="05:30:00":
                                            bmrcolor11="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            bmrcolor12="red"
                                            bmrcolor13="red"
                                            bmrcolor11="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            bmrcolor15="red"
                                            bmrcolor11="red"
                                            bmrcolor12="red"
                                            bmrcolor13="red"
                                            bmrcolor14="red"
                                    elif str(reservation.startTime)=="05:00:00":
                                        bmrcolor11="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor12="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            bmrcolor12="red"
                                            bmrcolor13="red"
                                            bmrcolor14="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            bmrcolor15="red"
                                            bmrcolor16="red"
                                            bmrcolor12="red"
                                            bmrcolor13="red"
                                            bmrcolor14="red"
                                    elif str(reservation.startTime)=="05:30:00":
                                        bmrcolor12="red"
                                        if str(reservation.endTime)=="06:30:00":
                                            bmrcolor13="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            bmrcolor15="red"
                                            bmrcolor13="red"
                                            bmrcolor14="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            bmrcolor15="red"
                                            bmrcolor16="red"
                                            bmrcolor17="red"
                                            bmrcolor13="red"
                                            bmrcolor14="red"
                                    elif str(reservation.startTime)=="06:00:00":
                                        bmrcolor13="red"
                                        if str(reservation.endTime)=="07:00:00":
                                            bmrcolor14="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            bmrcolor15="red"
                                            bmrcolor16="red"
                                            bmrcolor14="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor15="red"
                                            bmrcolor16="red"
                                            bmrcolor17="red"
                                            bmrcolor18="red"
                                            bmrcolor14="red"
                                    elif str(reservation.startTime)=="06:30:00":
                                        bmrcolor14="red"
                                        if str(reservation.endTime)=="07:30:00":
                                            bmrcolor15="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            bmrcolor15="red"
                                            bmrcolor16="red"
                                            bmrcolor17="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor15="red"
                                            bmrcolor16="red"
                                            bmrcolor17="red"
                                            bmrcolor18="red"
                                            bmrcolor19="red"
                                    elif str(reservation.startTime)=="07:00:00":
                                        bmrcolor15="red"
                                        if str(reservation.endTime)=="08:00:00":
                                            bmrcolor16="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor18="red"
                                            bmrcolor16="red"
                                            bmrcolor17="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor20="red"
                                            bmrcolor16="red"
                                            bmrcolor17="red"
                                            bmrcolor18="red"
                                            bmrcolor19="red"
                                    elif str(reservation.startTime)=="07:30:00":
                                        bmrcolor16="red"
                                        if str(reservation.endTime)=="08:30:00":
                                            bmrcolor17="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor18="red"
                                            bmrcolor19="red"
                                            bmrcolor17="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor20="red"
                                            bmrcolor21="red"
                                            bmrcolor17="red"
                                            bmrcolor18="red"
                                            bmrcolor19="red"
                                    elif str(reservation.startTime)=="08:00:00":
                                        bmrcolor17="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor18="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor18="red"
                                            bmrcolor19="red"
                                            bmrcolor20="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor20="red"
                                            bmrcolor21="red"
                                            bmrcolor22="red"
                                            bmrcolor18="red"
                                            bmrcolor19="red"
                                    elif str(reservation.startTime)=="08:30:00":
                                        bmrcolor18="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor19="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor21="red"
                                            bmrcolor19="red"
                                            bmrcolor20="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            bmrcolor20="red"
                                            bmrcolor21="red"
                                            bmrcolor22="red"
                                            bmrcolor23="red"
                                            bmrcolor19="red"
                                    elif str(reservation.startTime)=="09:00:00":
                                        bmrcolor19="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor20="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor21="red"
                                            bmrcolor22="red"
                                            bmrcolor20="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor20="red"
                                            bmrcolor21="red"
                                            bmrcolor22="red"
                                            bmrcolor23="red"
                                            bmrcolor24="red"
                                    elif str(reservation.startTime)=="09:30:00":
                                        bmrcolor20="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor21="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            bmrcolor21="red"
                                            bmrcolor22="red"
                                            bmrcolor23="red"
                                        if str(reservation.endTime)=="12:30:00":
                                            bmrcolor25="red"
                                            bmrcolor21="red"
                                            bmrcolor22="red"
                                            bmrcolor23="red"
                                            bmrcolor24="red"
                                    elif str(reservation.startTime)=="10:00:00":
                                        bmrcolor21="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor22="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor24="red"
                                            bmrcolor22="red"
                                            bmrcolor23="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor25="red"
                                            bmrcolor26="red"
                                            bmrcolor22="red"
                                            bmrcolor23="red"
                                            bmrcolor24="red"
                                    elif str(reservation.startTime)=="10:30:00":
                                        bmrcolor22="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor23="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor24="red"
                                            bmrcolor25="red"
                                            bmrcolor23="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor25="red"
                                            bmrcolor26="red"
                                            bmrcolor27="red"
                                            bmrcolor23="red"
                                            bmrcolor24="red"
                                    elif str(reservation.startTime)=="11:00:00":
                                        bmrcolor23="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor24="red"
                                        if str(reservation.endTime)=="12:00:00":
                                            bmrcolor24="red"
                                            bmrcolor25="red"
                                            bmrcolor26="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor25="red"
                                            bmrcolor26="red"
                                            bmrcolor27="red"
                                            bmrcolor28="red"
                                            bmrcolor24="red"
                                    elif str(reservation.startTime)=="11:30:00":
                                        bmrcolor24="red"
                                        if str(reservation.endTime)=="12:30:00":
                                            bmrcolor25="red"
                                        if str(reservation.endTime)=="13:30:00":
                                            bmrcolor27="red"
                                            bmrcolor25="red"
                                            bmrcolor26="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            bmrcolor25="red"
                                            bmrcolor26="red"
                                            bmrcolor27="red"
                                            bmrcolor28="red"
                                            bmrcolor29="red"




                                    elif str(reservation.startTime)=="12:00:00":
                                        bmrcolor25="red"
                                        if str(reservation.endTime)=="13:00:00":
                                            bmrcolor26="red"
                                        if str(reservation.endTime)=="14:00:00":
                                            bmrcolor26="red"
                                            bmrcolor27="red"
                                            bmrcolor28="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            bmrcolor26="red"
                                            bmrcolor27="red"
                                            bmrcolor28="red"
                                            bmrcolor29="red"
                                            bmrcolor30="red"
                                    elif str(reservation.startTime)=="12:30:00":
                                        bmrcolor2="red"
                                        if str(reservation.endTime)=="13:30:00":
                                            bmrcolor27="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            bmrcolor27="red"
                                            bmrcolor28="red"
                                            bmrcolor29="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            bmrcolor31="red"
                                            bmrcolor27="red"
                                            bmrcolor28="red"
                                            bmrcolor29="red"
                                            bmrcolor30="red"
                                    elif str(reservation.startTime)=="13:00:00":
                                        bmrcolor27="red"
                                        if str(reservation.endTime)=="14:00:00":
                                            bmrcolor28="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            bmrcolor28="red"
                                            bmrcolor29="red"
                                            bmrcolor30="red"
                                        if str(reservation.endTime)=="16:00:00":
                                            bmrcolor32="red"
                                            bmrcolor31="red"
                                            bmrcolor28="red"
                                            bmrcolor29="red"
                                            bmrcolor30="red"
                                    elif str(reservation.startTime)=="13:30:00":
                                        bmrcolor28="red"
                                        if str(reservation.endTime)=="14:30:00":
                                            bmrcolor29="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            bmrcolor29="red"
                                            bmrcolor30="red"
                                            bmrcolor31="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            bmrcolor29="red"
                                            bmrcolor30="red"
                                            bmrcolor31="red"
                                            bmrcolor32="red"
                                            bmrcolor33="red"
                                    elif str(reservation.startTime)=="14:00:00":
                                        bmrcolor29="red"
                                        if str(reservation.endTime)=="15:00:00":
                                            bmrcolor30="red"
                                        if str(reservation.endTime)=="06:00:00":
                                            bmrcolor30="red"
                                            bmrcolor31="red"
                                            bmrcolor32="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            bmrcolor34="red"
                                            bmrcolor30="red"
                                            bmrcolor31="red"
                                            bmrcolor32="red"
                                            bmrcolor33="red"
                                    elif str(reservation.startTime)=="14:30:00":
                                        bmrcolor30="red"
                                        if str(reservation.endTime)=="15:30:00":
                                            bmrcolor31="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            bmrcolor33="red"
                                            bmrcolor31="red"
                                            bmrcolor32="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            bmrcolor34="red"
                                            bmrcolor35="red"
                                            bmrcolor31="red"
                                            bmrcolor32="red"
                                            bmrcolor33="red"
                                    elif str(reservation.startTime)=="15:00:00":
                                        bmrcolor31="red"
                                        if str(reservation.endTime)=="16:00:00":
                                            bmrcolor32="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            bmrcolor33="red"
                                            bmrcolor34="red"
                                            bmrcolor32="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            bmrcolor34="red"
                                            bmrcolor35="red"
                                            bmrcolor12="red"
                                            bmrcolor32="red"
                                            bmrcolor33="red"
                                    elif str(reservation.startTime)=="15:30:00":
                                        bmrcolor32="red"
                                        if str(reservation.endTime)=="16:30:00":
                                            bmrcolor33="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            bmrcolor33="red"
                                            bmrcolor34="red"
                                            bmrcolor35="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            bmrcolor34="red"
                                            bmrcolor35="red"
                                            bmrcolor36="red"
                                            bmrcolor37="red"
                                            bmrcolor33="red"
                                    elif str(reservation.startTime)=="16:00:00":
                                        bmrcolor33="red"
                                        if str(reservation.endTime)=="17:00:00":
                                            bmrcolor34="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            bmrcolor36="red"
                                            bmrcolor34="red"
                                            bmrcolor35="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            bmrcolor34="red"
                                            bmrcolor35="red"
                                            bmrcolor36="red"
                                            bmrcolor37="red"
                                            bmrcolor38="red"
                                    elif str(reservation.startTime)=="16:30:00":
                                        bmrcolor34="red"
                                        if str(reservation.endTime)=="17:30:00":
                                            bmrcolor35="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            bmrcolor36="red"
                                            bmrcolor37="red"
                                            bmrcolor35="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            bmrcolor39="red"
                                            bmrcolor35="red"
                                            bmrcolor36="red"
                                            bmrcolor37="red"
                                            bmrcolor38="red"
                                    elif str(reservation.startTime)=="17:00:00":
                                        bmrcolor35="red"
                                        if str(reservation.endTime)=="18:00:00":
                                            bmrcolor36="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            bmrcolor36="red"
                                            bmrcolor37="red"
                                            bmrcolor38="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            bmrcolor39="red"
                                            bmrcolor40="red"
                                            bmrcolor36="red"
                                            bmrcolor37="red"
                                            bmrcolor38="red"
                                    elif str(reservation.startTime)=="17:30:00":
                                        bmrcolor36="red"
                                        if str(reservation.endTime)=="18:30:00":
                                            bmrcolor37="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            bmrcolor39="red"
                                            bmrcolor37="red"
                                            bmrcolor38="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            bmrcolor39="red"
                                            bmrcolor40="red"
                                            bmrcolor41="red"
                                            bmrcolor37="red"
                                            bmrcolor38="red"
                                    elif str(reservation.startTime)=="18:00:00":
                                        bmrcolor37="red"
                                        if str(reservation.endTime)=="19:00:00":
                                            bmrcolor38="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            bmrcolor39="red"
                                            bmrcolor40="red"
                                            bmrcolor38="red"
                                        if str(reservation.endTime)=="21:00:00":
                                            bmrcolor39="red"
                                            bmrcolor40="red"
                                            bmrcolor41="red"
                                            bmrcolor42="red"
                                            bmrcolor38="red"
                                    elif str(reservation.startTime)=="18:30:00":
                                        bmrcolor38="red"
                                        if str(reservation.endTime)=="19:30:00":
                                            bmrcolor39="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            bmrcolor39="red"
                                            bmrcolor40="red"
                                            bmrcolor41="red"
                                        if str(reservation.endTime)=="21:30:00":
                                            bmrcolor39="red"
                                            bmrcolor40="red"
                                            bmrcolor41="red"
                                            bmrcolor42="red"
                                            bmrcolor43="red"
                                    elif str(reservation.startTime)=="19:00:00":
                                        bmrcolor39="red"
                                        if str(reservation.endTime)=="20:00:00":
                                            bmrcolor40="red"
                                        if str(reservation.endTime)=="21:00:00":
                                            bmrcolor42="red"
                                            bmrcolor40="red"
                                            bmrcolor41="red"
                                        if str(reservation.endTime)=="22:00:00":
                                            bmrcolor44="red"
                                            bmrcolor40="red"
                                            bmrcolor41="red"
                                            bmrcolor42="red"
                                            bmrcolor43="red"
                                    elif str(reservation.startTime)=="19:30:00":
                                        bmrcolor40="red"
                                        if str(reservation.endTime)=="20:30:00":
                                            bmrcolor41="red"
                                        if str(reservation.endTime)=="21:30:00":
                                            bmrcolor42="red"
                                            bmrcolor43="red"
                                            bmrcolor41="red"
                                        if str(reservation.endTime)=="22:30:00":
                                            bmrcolor44="red"
                                            bmrcolor45="red"
                                            bmrcolor41="red"
                                            bmrcolor42="red"
                                            bmrcolor43="red"
                                    elif str(reservation.startTime)=="08:00:00":
                                        bmrcolor41="red"
                                        if str(reservation.endTime)=="09:00:00":
                                            bmrcolor42="red"
                                        if str(reservation.endTime)=="10:00:00":
                                            bmrcolor42="red"
                                            bmrcolor43="red"
                                            bmrcolor44="red"
                                        if str(reservation.endTime)=="11:00:00":
                                            bmrcolor44="red"
                                            bmrcolor45="red"
                                            bmrcolor46="red"
                                            bmrcolor42="red"
                                            bmrcolor43="red"
                                    elif str(reservation.startTime)=="08:30:00":
                                        bmrcolor42="red"
                                        if str(reservation.endTime)=="09:30:00":
                                            bmrcolor43="red"
                                        if str(reservation.endTime)=="10:30:00":
                                            bmrcolor45="red"
                                            bmrcolor43="red"
                                            bmrcolor44="red"
                                        if str(reservation.endTime)=="11:30:00":
                                            bmrcolor44="red"
                                            bmrcolor45="red"
                                            bmrcolor46="red"
                                            bmrcolor47="red"
                                            bmrcolor43="red"
                                    elif str(reservation.startTime)=="21:00:00":
                                        bmrcolor43="red"
                                        if str(reservation.endTime)=="22:00:00":
                                            bmrcolor44="red"
                                        if str(reservation.endTime)=="23:00:00":
                                            bmrcolor45="red"
                                            bmrcolor46="red"
                                            bmrcolor44="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            bmrcolor44="red"
                                            bmrcolor45="red"
                                            bmrcolor46="red"
                                            bmrcolor47="red"
                                            bmrcolor48="red"
                                    elif str(reservation.startTime)=="21:30:00":
                                        bmrcolor44="red"
                                        if str(reservation.endTime)=="22:30:00":
                                            bmrcolor45="red"
                                        if str(reservation.endTime)=="23:30:00":
                                            bmrcolor45="red"
                                            bmrcolor46="red"
                                            bmrcolor47="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            #bmrcolor25="red"
                                            bmrcolor45="red"
                                            bmrcolor46="red"
                                            bmrcolor47="red"
                                            bmrcolor48="red"
                                    elif str(reservation.startTime)=="22:00:00":
                                        bmrcolor45="red"
                                        if str(reservation.endTime)=="23:00:00":
                                            bmrcolor46="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            bmrcolor48="red"
                                            bmrcolor46="red"
                                            bmrcolor47="red"
                                        if str(reservation.endTime)=="1:00:00":
                                            #bmrcolor25="red"
                                            #bmrcolor26="red"
                                            bmrcolor46="red"
                                            bmrcolor47="red"
                                            bmrcolor48="red"
                                    elif str(reservation.startTime)=="22:30:00":
                                        bmrcolor46="red"
                                        if str(reservation.endTime)=="23:30:00":
                                            bmrcolor47="red"
                                        if str(reservation.endTime)=="00:30:00":
                                            bmrcolor48="red"
                                            #bmrcolor25="red"
                                            bmrcolor47="red"
                                        if str(reservation.endTime)=="01:30:00":
                                            #bmrcolor25="red"
                                            #bmrcolor26="red"
                                            #bmrcolor27="red"
                                            bmrcolor47="red"
                                            bmrcolor48="red"
                                    elif str(reservation.startTime)=="23:00:00":
                                        bmrcolor47="red"
                                        if str(reservation.endTime)=="00:00:00":
                                            bmrcolor48="red"
                                        if str(reservation.endTime)=="01:00:00":
                                            bmrcolor48="red"
                                            #bmrcolor25="red"
                                            #bmrcolor26="red"
                                        if str(reservation.endTime)=="02:00:00":
                                            #bmrcolor25="red"
                                            #bmrcolor26="red"
                                            #bmrcolor27="red"
                                            #bmrcolor28="red"
                                            bmrcolor48="red"
                                    elif str(reservation.startTime)=="23:30:00":
                                        bmrcolor48="red"
                                        #if str(reservation.endTime)=="00:30:00":
                                            #bmrcolor25="red"
                                        #elif str(reservation.endTime)=="01:30:00":
                                            #bmrcolor27="red"
                                            #bmrcolor25="red"
                                            #bmrcolor26="red"
                                        #elif str(r.endTime)=="02:30:00":
                                            #bmrcolor25="red"
                                            #trcolor26="red"
                                            #bmrcolor27="red"
                                            #bmrcolor28="red"
                                            #bmrcolor29="red"

                return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,
                'smrcolor1':smrcolor1,'smrcolor2':smrcolor2,'smrcolor3':smrcolor3,'smrcolor4':smrcolor4,'smrcolor5':smrcolor5,'smrcolor6':smrcolor6,'smrcolor7':smrcolor7,
                'smrcolor8':smrcolor8,'smrcolor9':smrcolor9,'smrcolor10':smrcolor10,'smrcolor11':smrcolor11,'smrcolor12':smrcolor12,'smrcolor13':smrcolor13,
                'smrcolor14':smrcolor14,'smrcolor15':smrcolor15,'smrcolor16':smrcolor16,'smrcolor17':smrcolor17,'smrcolor18':smrcolor18,'smrcolor19':smrcolor19,
                'smrcolor20':smrcolor20,'smrcolor21':smrcolor21,'smrcolor22':smrcolor22,'smrcolor23':smrcolor23,'smrcolor24':smrcolor24,'smrcolor25':smrcolor25,
                'smrcolor26':smrcolor26,'smrcolor27':smrcolor27,'smrcolor28':smrcolor28,'smrcolor29':smrcolor29,'smrcolor30':smrcolor30,'smrcolor31':smrcolor31,
                'smrcolor32':smrcolor32,'smrcolor33':smrcolor33,'smrcolor34':smrcolor34,'smrcolor35':smrcolor35,'smrcolor36':smrcolor36,'smrcolor37':smrcolor37,
                'smrcolor38':smrcolor38,'smrcolor39':smrcolor39,'smrcolor40':smrcolor40,'smrcolor41':smrcolor41,'smrcolor42':smrcolor42,'smrcolor43':smrcolor43,
                'smrcolor44':smrcolor44,'smrcolor45':smrcolor45,'smrcolor46':smrcolor46,'smrcolor47':smrcolor47,'smrcolor48':smrcolor48,

                'trcolor1':trcolor1,'trcolor2':trcolor2,'trcolor3':trcolor3,'trcolor4':trcolor4,'trcolor5':trcolor5,'trcolor6':trcolor6,'trcolor7':trcolor7,
                'trcolor8':trcolor8,'trcolor9':trcolor9,'trcolor10':trcolor10,'trcolor11':trcolor11,'trcolor12':trcolor12,'trcolor13':trcolor13,
                'trcolor14':trcolor14,'trcolor15':trcolor15,'trcolor16':trcolor16,'trcolor17':trcolor17,'trcolor18':trcolor18,'trcolor19':trcolor19,
                'trcolor20':trcolor20,'trcolor21':trcolor21,'trcolor22':trcolor22,'trcolor23':trcolor23,'trcolor24':trcolor24,'trcolor25':trcolor25,
                'trcolor26':trcolor26,'trcolor27':trcolor27,'trcolor28':trcolor28,'trcolor29':trcolor29,'trcolor30':trcolor30,'trcolor31':trcolor31,
                'trcolor32':trcolor32,'trcolor33':trcolor33,'trcolor34':trcolor34,'trcolor35':trcolor35,'trcolor36':trcolor36,'trcolor37':trcolor37,
                'trcolor38':trcolor38,'trcolor39':trcolor39,'trcolor40':trcolor40,'trcolor41':trcolor41,'trcolor42':trcolor42,'trcolor43':trcolor43,
                'trcolor44':trcolor44,'trcolor45':trcolor45,'trcolor46':trcolor46,'trcolor47':trcolor47,'trcolor48':trcolor48,

                'bmrcolor1':bmrcolor1,'bmrcolor2':bmrcolor2,'bmrcolor3':bmrcolor3,'bmrcolor4':bmrcolor4,'bmrcolor5':bmrcolor5,'bmrcolor6':bmrcolor6,'bmrcolor7':bmrcolor7,
                'bmrcolor8':bmrcolor8,'bmrcolor9':bmrcolor9,'bmrcolor10':bmrcolor10,'bmrcolor11':bmrcolor11,'bmrcolor12':bmrcolor12,'bmrcolor13':bmrcolor13,
                'bmrcolor14':bmrcolor14,'bmrcolor15':bmrcolor15,'bmrcolor16':bmrcolor16,'bmrcolor17':bmrcolor17,'bmrcolor18':bmrcolor18,'bmrcolor19':bmrcolor19,
                'bmrcolor20':bmrcolor20,'bmrcolor21':bmrcolor21,'bmrcolor22':bmrcolor22,'bmrcolor23':bmrcolor23,'bmrcolor24':bmrcolor24,'bmrcolor25':bmrcolor25,
                'bmrcolor26':bmrcolor26,'bmrcolor27':bmrcolor27,'bmrcolor28':bmrcolor28,'bmrcolor29':bmrcolor29,'bmrcolor30':bmrcolor30,'bmrcolor31':bmrcolor31,
                'bmrcolor32':bmrcolor32,'bmrcolor33':bmrcolor33,'bmrcolor34':bmrcolor34,'bmrcolor35':bmrcolor35,'bmrcolor36':bmrcolor36,'bmrcolor37':bmrcolor37,
                'bmrcolor38':bmrcolor38,'bmrcolor39':bmrcolor39,'bmrcolor40':bmrcolor40,'bmrcolor41':bmrcolor41,'bmrcolor42':bmrcolor42,'bmrcolor43':bmrcolor43,
                'bmrcolor44':bmrcolor44,'bmrcolor45':bmrcolor45,'bmrcolor46':bmrcolor46,'bmrcolor47':bmrcolor47,'bmrcolor48':bmrcolor48,
            })

        else:
            print('error')

    return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,
    'smrcolor1':smrcolor1,'smrcolor2':smrcolor2,'smrcolor3':smrcolor3,'smrcolor4':smrcolor4,'smrcolor5':smrcolor5,'smrcolor6':smrcolor6,'smrcolor7':smrcolor7,
    'smrcolor8':smrcolor8,'smrcolor9':smrcolor9,'smrcolor10':smrcolor10,'smrcolor11':smrcolor11,'smrcolor12':smrcolor12,'smrcolor13':smrcolor13,
    'smrcolor14':smrcolor14,'smrcolor15':smrcolor15,'smrcolor16':smrcolor16,'smrcolor17':smrcolor17,'smrcolor18':smrcolor18,'smrcolor19':smrcolor19,
    'smrcolor20':smrcolor20,'smrcolor21':smrcolor21,'smrcolor22':smrcolor22,'smrcolor23':smrcolor23,'smrcolor24':smrcolor24,'smrcolor25':smrcolor25,
    'smrcolor26':smrcolor26,'smrcolor27':smrcolor27,'smrcolor28':smrcolor28,'smrcolor29':smrcolor29,'smrcolor30':smrcolor30,'smrcolor31':smrcolor31,
    'smrcolor32':smrcolor32,'smrcolor33':smrcolor33,'smrcolor34':smrcolor34,'smrcolor35':smrcolor35,'smrcolor36':smrcolor36,'smrcolor37':smrcolor37,
    'smrcolor38':smrcolor38,'smrcolor39':smrcolor39,'smrcolor40':smrcolor40,'smrcolor41':smrcolor41,'smrcolor42':smrcolor42,'smrcolor43':smrcolor43,
    'smrcolor44':smrcolor44,'smrcolor45':smrcolor45,'smrcolor46':smrcolor46,'smrcolor47':smrcolor47,'smrcolor48':smrcolor48,

    'trcolor1':trcolor1,'trcolor2':trcolor2,'trcolor3':trcolor3,'trcolor4':trcolor4,'trcolor5':trcolor5,'trcolor6':trcolor6,'trcolor7':trcolor7,
    'trcolor8':trcolor8,'trcolor9':trcolor9,'trcolor10':trcolor10,'trcolor11':trcolor11,'trcolor12':trcolor12,'trcolor13':trcolor13,
    'trcolor14':trcolor14,'trcolor15':trcolor15,'trcolor16':trcolor16,'trcolor17':trcolor17,'trcolor18':trcolor18,'trcolor19':trcolor19,
    'trcolor20':trcolor20,'trcolor21':trcolor21,'trcolor22':trcolor22,'trcolor23':trcolor23,'trcolor24':trcolor24,'trcolor25':trcolor25,
    'trcolor26':trcolor26,'trcolor27':trcolor27,'trcolor28':trcolor28,'trcolor29':trcolor29,'trcolor30':trcolor30,'trcolor31':trcolor31,
    'trcolor32':trcolor32,'trcolor33':trcolor33,'trcolor34':trcolor34,'trcolor35':trcolor35,'trcolor36':trcolor36,'trcolor37':trcolor37,
    'trcolor38':trcolor38,'trcolor39':trcolor39,'trcolor40':trcolor40,'trcolor41':trcolor41,'trcolor42':trcolor42,'trcolor43':trcolor43,
    'trcolor44':trcolor44,'trcolor45':trcolor45,'trcolor46':trcolor46,'trcolor47':trcolor47,'trcolor48':trcolor48,

    'bmrcolor1':bmrcolor1,'bmrcolor2':bmrcolor2,'bmrcolor3':bmrcolor3,'bmrcolor4':bmrcolor4,'bmrcolor5':bmrcolor5,'bmrcolor6':bmrcolor6,'bmrcolor7':bmrcolor7,
    'bmrcolor8':bmrcolor8,'bmrcolor9':bmrcolor9,'bmrcolor10':bmrcolor10,'bmrcolor11':bmrcolor11,'bmrcolor12':bmrcolor12,'bmrcolor13':bmrcolor13,
    'bmrcolor14':bmrcolor14,'bmrcolor15':bmrcolor15,'bmrcolor16':bmrcolor16,'bmrcolor17':bmrcolor17,'bmrcolor18':bmrcolor18,'bmrcolor19':bmrcolor19,
    'bmrcolor20':bmrcolor20,'bmrcolor21':bmrcolor21,'bmrcolor22':bmrcolor22,'bmrcolor23':bmrcolor23,'bmrcolor24':bmrcolor24,'bmrcolor25':bmrcolor25,
    'bmrcolor26':bmrcolor26,'bmrcolor27':bmrcolor27,'bmrcolor28':bmrcolor28,'bmrcolor29':bmrcolor29,'bmrcolor30':bmrcolor30,'bmrcolor31':bmrcolor31,
    'bmrcolor32':bmrcolor32,'bmrcolor33':bmrcolor33,'bmrcolor34':bmrcolor34,'bmrcolor35':bmrcolor35,'bmrcolor36':bmrcolor36,'bmrcolor37':bmrcolor37,
    'bmrcolor38':bmrcolor38,'bmrcolor39':bmrcolor39,'bmrcolor40':bmrcolor40,'bmrcolor41':bmrcolor41,'bmrcolor42':bmrcolor42,'bmrcolor43':bmrcolor43,
    'bmrcolor44':bmrcolor44,'bmrcolor45':bmrcolor45,'bmrcolor46':bmrcolor46,'bmrcolor47':bmrcolor47,'bmrcolor48':bmrcolor48,
})

@login_required
def reservations(request):
    user = request.user
    res_list = Reservation.objects.filter(user=request.user)

    #for r in res_list :
    #    listres = []
    #    print(r.user)

    #    if r.user.username == user:
    #        listres.append(r)
    dict= {'listres':res_list}
    return render(request,'myreservations.html',{'res_list':res_list})

@login_required
def home(request):
    postitform = forms.postitform()
    postits=Postit.objects.all()
    if request.method == 'POST':
        postitform= forms.postitform(request.POST)
        if postitform.is_valid:
            postit =postitform.save(commit=False)
            postit.user=request.user
            postit.save()
            return render(request,'home.html',{'postitform':postitform,'postits':postits})

    return render(request,'home.html',{'postitform':postitform,'postits':postits})

@login_required
def admin(request):
    liste = Reservation.objects.filter(isValidated=False)
    lis =Reservation.objects.all()
    listeUsers=User.objects.filter(is_active=False)
    return render(request,'admin.html',{'liste':liste,'listeUsers':listeUsers,'lis':lis})

@login_required
def deletereserv(request,reservation_id=None):
    res= Reservation.objects.get(id=reservation_id)
    res.delete()
    return HttpResponseRedirect(reverse('reservations'))


@login_required
def validate(request, reservation_id=None):
    res=Reservation.objects.get(id=reservation_id)
    res.isValidated=True
    res.save()
    return HttpResponseRedirect(reverse('reservations'))

@login_required
def validateuser(request,user_id=None):
    us=User.objects.get(id=user_id)
    us.is_active=True
    us.save()
    current_site = get_current_site(request)
    mail_subject = 'B@Labs reservation platform - Account'
    message = render_to_string('acc_active_email.html', {
                'user': us,
                'domain': current_site.domain,

            })
    to_email = us.email
    email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
    email.send()
    return HttpResponseRedirect(reverse('adminusers'))

@login_required
def deleteuser(request,user_id=None):
    us=User.objects.get(id=user_id)
    print(us)
    current_site = get_current_site(request)
    mail_subject = 'Your account is deleted'
    message = render_to_string('deletedUser.html', {
                'user': us,
                'domain': current_site.domain,

            })
    to_email = us.email
    email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
    email.send()
    us.delete()
    return HttpResponseRedirect(reverse('seeusers'))

@login_required
def adminusers(request):
        listeUsers=User.objects.filter(is_active=False)
        return render(request,'validation-users.html',{'listeUsers':listeUsers,})

@login_required
def adminreservations(request):
        liste = Reservation.objects.filter(isValidated=False)
        return render(request,'validation-reservations.html',{'liste':liste})


@login_required
def notespage(request):
    needform = forms.needform()
    message = "Your opinion and ideas are our inspiration"
    if request.method == 'POST':

        needform= forms.needform(request.POST)

        if needform.is_valid():
            need =needform.save(commit=False)
            need.user=request.user

            need.save()
            message="Thank you for contributing in making our space amazing !"
            return render(request,'need.html',{'needform':needform,'message':message})

        else :
            print("error")
    return render(request,'need.html',{'needform':needform,'message':message})

@login_required
def deletenote(request,note_id=None):
    res= Need.objects.get(id=note_id)
    res.delete()
    return HttpResponseRedirect(reverse('seenotes'))


@login_required
def lockers(request):
    message =""
    users=User.objects.all()
    lockers=Locker.objects.filter(isFree=True)
    if request.method == 'POST':
        user= User.objects.get(id=int(request.POST.get('user')))
        locker= Locker.objects.get(id=int(request.POST.get('locker')))

        locker.user=user
        locker.isFree=False
        locker.save()
        message= str(user)+" now has the locker "+str(locker.reference)
        return render(request,'adminlockers.html',{'users':users,'lockers':lockers,'message':message})

    return render(request,'adminlockers.html',{'users':users,'lockers':lockers,'message':message})

@login_required
def reservelocker(request):
    message =""
    users=UserInfo.objects.all()
    lockers=Locker.objects.filter(isFree=True)
    current_user=request.user.id
    print(current_user)
    mylockers=Locker.objects.filter(user_id=current_user)
    if request.method == 'POST' :
        user= request.user
        locker=Locker.objects.get(id=int(request.POST.get('locker')))
        locker.user= user
        locker.isFree=False
        locker.adminValid=False
        locker.save()
        message="Waiting for admin to validate !"
        return render(request,'reservelocker.html',{'users':users,'lockers':lockers,'message':message,'mylockers':mylockers})
    return render(request,'reservelocker.html',{'users':users,'lockers':lockers,'message':message,'mylockers':mylockers})

@login_required
def adminlockers(request):
    locker=Locker.objects.filter(adminValid=False)
    lockers=[]
    for l in locker:
        if l.user != None:
            lockers.append(l)
    return render(request, 'validation-lockers.html',{'lockers':lockers,})

@login_required
def deletelocker(request,locker_id=None):
    locker= Locker.objects.get(id=locker_id)
    locker.isFree=True
    locker.adminValid=False
    locker.user=None
    locker.save()
    return HttpResponseRedirect(reverse('adminlockers'))


@login_required
def validatelockers(request, locker_id=None):
    locker=Locker.objects.get(id=locker_id)
    locker.adminValid=True
    locker.save()
    return HttpResponseRedirect(reverse('adminlockers'))

@login_required
def seereservations(request):
    lis=Reservation.objects.all()
    return render(request,'visualize-reservations.html',{'lis':lis,})

@login_required
def seeusers(request):
    lis=User.objects.all()
    return render(request,'visualize-users.html',{'lis':lis,})


@login_required
def seenotes(request):
    noteslist=Need.objects.all()
    return render(request,'visualize-notes.html',{'noteslist':noteslist,})

@login_required
def seelockers(request):
    lockers=Locker.objects.all()
    return render(request,'visualize-lockers.html',{'lockers':lockers,})


@login_required
def seevisitors(request):
    visitors=Visitor.objects.all()
    return render(request,'visualize-visitors.html',{"visitors":visitors})

@login_required
def makepresence(request):
    presenceform = forms.presenceform()
    startups = Startup.objects.all()
    if request.method == "POST" :
            number =request.POST.get('number')
            iid =request.POST.get('id')
            print("here")
            s= Startup.objects.get(id=iid)
            print(s.name)
            date = datetime.date.today()
            time = datetime.datetime.now()

            presence = Presence(number=number,startup=s,time=time,date=date)
            print("last check")

            presence.save()

            return render(request,'validation-presence.html',{'presenceform':presenceform,'startups':startups})
    else:
            print("No, invalid form dumbass !")

    return render(request,'validation-presence.html',{'presenceform':presenceform,'startups':startups})

@login_required
def stats_presence(request):
    queryset = Presence.objects.all()
    s = ['startup']
    n=['']
    timespot =datetime.datetime.strptime('Jun 1 2005  8:00AM', '%b %d %Y %I:%M%p').time()

    for c in Presence.objects.all():
        if not(c.startup.name in s):
            avg = Presence.objects.filter(startup=c.startup).aggregate(Avg('number')).get('number__avg')
            s.append(c.startup.name)
            n.append(avg)

    data_source = ModelDataSource(queryset,fields=['time','number'])
    chart = gchart.LineChart(data_source, options={'title': "Correlation of time and number of present people", 'xaxis': {'mode': "categories"}})

    data_source2=[]
    data_source2=[s,n]
    print(data_source2)
    chart2 = gchart.ColumnChart(SimpleDataSource(data=data_source2), options={'title': "Average of present people per startup", 'xaxis': {'mode': "categories"}})
    return render(request,"stats-presence.html",{'chart':chart,'chart2':chart2})


@login_required
def stats_reservation(request):
    return render(request,'stats-reservations.html')

def test(request):

    return render(request,'test.html')

@login_required
def add_workshop(request):
    form = addworkshop()
    msg=''
    itIs = False
    if (request.method == "POST"):
        form = addworkshop(data=request.POST)
        if form.is_valid():
            workshop=form.save(commit=False)
            if (workshop.otherTheme != None):
                workshop.theme = workshop.otherTheme
            workshop.save()
            msg="Workshop saved successully !"
            itIs=True
            return render(request,'add-workshop.html',{'form':form,'msg':msg,'itIs':itIs})

    return render(request,'add-workshop.html',{'form':form,'msg':msg,'itIs':itIs})

@login_required
def workshops(request):
    wks = Workshop.objects.all()


    return render(request,'visualize-workshops.html',{'wks':wks,})

@login_required
def deletewks(request,workshop_id=None):
    res= Workshop.objects.get(id=workshop_id)
    res.delete()
    return HttpResponseRedirect(reverse('workshops'))

@login_required
def validatewks(request,workshop_id=None):
    wks=Workshop.objects.get(id=workshop_id)
    wks.isDone=True
    wks.save()
    return HttpResponseRedirect(reverse('workshops'))

@login_required
def myworkshops(request):
    req = Workshop.objects.filter(isDone=False)
    return render(request,'myworkshops.html',{'req':req})

@login_required
def presencewks(request,workshop_id=None):
    wks = Workshop.objects.get(id=workshop_id)
    stps=[]
    stpss=wks.startups.all()
    stpsss = Startup.objects.all()
    for s in stpsss:
        if not(s in stpss) :
            stps.append(s)


    return render(request,'presencewks.html',{'wks':wks,'stps':stps,'stpss':stpss})

@login_required
def addwkspresence(request,workshop_id=None,startup_id=None):
    stp = Startup.objects.get(id = startup_id)
    wks = Workshop.objects.get(id = workshop_id)
    wks.startups.add(stp)
    return HttpResponseRedirect(reverse('presencewks',args=(wks.id,)))

@login_required
def evaluate(request,startup_id=None):
    form = forms.evaluationform()
    s=Startup.objects.get(id=startup_id)
    if (request.method == "POST"):
        form = evaluationform(data=request.POST)
        print(form)
        if form.is_valid():
            evaluation=form.save(commit=False)
            evaluation.startup=s
            evaluation.save()
            return render(request,'evaluate.html',{'form':form,'s':s})
    return render(request,'evaluate.html',{'form':form,'s':s})

@login_required
def getoc(request):
        modules= Module.objects.filter(isActive=True).order_by('number')
        courses=Course.objects.all()
        state = False
        return render(request,'oc.html',{'modules':modules,'courses':courses,'state':state})

@login_required
def objectives(request,startup_id=None,week=None):
    s = Startup.objects.get(id=startup_id)
    obj = Objective.objects.filter(startup=s,week=week)
    form = forms.objectiveform()
    if (request.method) == "POST":
        form=objectiveform(data=request.POST)
        if form.is_valid() :
            objective = form.save(commit=False)
            objective.startup = s
            objective.week=week
            objective.save()
            return HttpResponseRedirect(reverse('objectives', kwargs={'startup_id':startup_id,'week':week}))
    if request.user.is_staff:
        return render(request,'objectives.html',{'s':s,'obj':obj,'form':form,'week':week})
    else:
        s=Startup.objects.get(id=request.user.userinfo.startup.id)
        return render(request,'objectives.html',{'s':s,'obj':obj,'form':form,'week':week})


@login_required
def getStartups(request):
    stps = Startup.objects.all()
    return render(request, 'startupsPortal.html',{'stps':stps})

@login_required
def objectiveDone(request,obj_id=None,startup_id=None,week=None):
    object= Objective.objects.get(id=obj_id)
    object.isDone=True
    object.save()
    return HttpResponseRedirect(reverse('objectives', kwargs={'startup_id':startup_id,'week':week}))

@login_required
def stpredirect(request):
    if request.user.is_staff:
            stps = Startup.objects.all()
            return render(request, 'startupsPortal.html',{'stps':stps})
    else:
        startup_id=request.user.userinfo.startup.id
        week=1
        return HttpResponseRedirect(reverse('objectives', kwargs={'startup_id':startup_id,'week':week}))


@login_required
def profile(request,user_id=None):
    u = User.objects.get(id=user_id)
    form = PassForm()
    if request.method=='POST':
        form = PassForm(data=request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            u.set_password(user.password)
            u.save()
            logout(request)
            return HttpResponseRedirect(reverse('index2'))

    return render(request,'profile.html',{'u':u,'form':form,})

@login_required
def main(request):
    return render(request,'FrontEnd/index.html')

@login_required
def stport(request):
    reservationform= forms.reserve()
    message =""
    users=UserInfo.objects.all()
    lockers=Locker.objects.filter(isFree=True)
    current_user=request.user.id
    print(current_user)
    mylockers=Locker.objects.filter(user_id=current_user)

    return render(request,'FrontEnd/startups/startups_base.html',{'reservationform':reservationform,'lockers':lockers,'message':message,'mylockers':mylockers})
