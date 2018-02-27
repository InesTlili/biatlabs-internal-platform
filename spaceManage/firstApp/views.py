from django.shortcuts import render
from datetime import timedelta
import datetime
import time

from firstApp.models import UserInfo, Reservation,Need,Module,Content,Course
from . import forms
from firstApp.forms import UserForm,ProfileForm,reserve,needform

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
# Create your views here.

def try2(request):
    modules= Module.objects.order_by('number')
    courses=Course.objects.all()
    return render(request,'base2.html',{'modules':modules,'courses':courses})


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
    print(course)
    return render(request,'course.html',{'cont':cont,'modules':modules,'courses':courses,'course':course})









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
        Profileform = ProfileForm(data=request.POST)

        if Userform.is_valid() and Profileform.is_valid():

            user=Userform.save(commit=False)
            user.set_password(user.password)
            user.is_active=False
            user.save()

            profile=Profileform.save(commit=False)
            profile.user=user
            profile.save()



            return HttpResponse('We will send you an email as soon as your account gets activated !')
            registered=True

        else :
            print(Userform.errors,Profileform.errors)

    else :
        Userform=UserForm()
        Profileform=ProfileForm()

    return render(request,'signup.html',{'Userform':Userform,'Profileform':Profileform,'registered':registered})


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
                return HttpResponseRedirect(reverse('reserve'))
            else :
                return HttpResponse("Account not active !")

        else :
            print("Username : {} and Password : {}".format(username,password))
            return HttpResponse("Login Failed Successfully ! :D")
    else:
        return render(request,'login.html',{})


@login_required
def userlogout(request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in, nice ! :-)")



@login_required
def reserve(request):
    reservationform= forms.reserve()
    res_list = Reservation.objects.order_by('space')
    message = "Reserve "
    if request.method == "POST":
        reservationform= forms.reserve(request.POST)
        #Multi Access management
        for r in res_list :
            if r.typeOf == request.POST.get('typeOf') :

                if (str(r.date) == (datetime.datetime.strptime(request.POST.get('date'),'%m/%d/%Y').strftime('%Y-%m-%d'))):
                    print("here")
                    if (datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time() == r.startTime):
                        message = "A meeting starts at this time ! Room reserved !"
                        return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message})
                    else :
                        if int(request.POST.get('extraTime'))>0 :
                            end=((datetime.datetime.combine(datetime.date(12, 12, 10), r.startTime) + datetime.timedelta(minutes=int(r.duration))).time())
                            formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(hours=int(request.POST.get('extraTime')))).time())

                        else:
                            end=((datetime.datetime.combine(datetime.date(12, 12, 10), r.startTime) + datetime.timedelta(minutes=int(r.duration))).time())
                            formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(minutes=int(request.POST.get('duration')))).time())

                        if  (datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time() > r.startTime and datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()<end) :
                            message = "A meeting is taking place at this time !"
                            return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message})
                        elif (formend>r.startTime and datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()<end):
                            message = "A meeting is taking place at this time !"
                            return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message})
                    #End of multi-access management function
        if reservationform.is_valid():
            formend = ((datetime.datetime.combine(datetime.date(12, 12, 10), datetime.datetime.strptime(request.POST.get('startTime'),'%H:%M').time()) + datetime.timedelta(minutes=int(request.POST.get('duration')))).time())
            #reservation = Reservation(**reservationform.cleaned_data,user=user)
            reservation =reservationform.save(commit=False)
            reservation.user=request.user
            reservation.endTime = formend
            if int(reservation.extraTime)>0:
                message = "Reservation pending till admin validates !"
                reservation.isValidated=False
                reservation.save()
                return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message})
            else:
                reservation.save()
                message = "Reservation recorded successfully !"
                return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message})

        else:
            print('error')
    return render(request,'reserve.html',{'reservationform':reservationform,'r_list':res_list,'message':message,})
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
def admin(request):
    liste = Reservation.objects.filter(isValidated=False)
    lis =Reservation.objects.all()
    listeUsers=User.objects.filter(is_active=False)
    print(listeUsers)
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
    return HttpResponseRedirect(reverse('admin'))

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
    return HttpResponseRedirect(reverse('admin'))


@login_required
def deleteuser(request,user_id=None):
    us=User.objects.get(id=user_id)

    current_site = get_current_site(request)
    mail_subject = 'Your account is active'
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
    return HttpResponseRedirect(reverse('admin'))

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

    if request.method == 'POST':

        needform= forms.needform(request.POST)

        if needform.is_valid():
            need =needform.save(commit=False)
            need.user=request.user

            need.save()
        else :
            print("error")
    return render(request,'need.html',{'needform':needform})
