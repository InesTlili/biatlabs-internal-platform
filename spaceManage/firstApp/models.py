from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SPACE_CHOICE=(('B@Labs - Av. Habib Bourguiba','B@Labs - Av. Habib Bourguiba'),)
TYPEOF_CHOICE=(('Small meeting room','Small meeting room'),('Training Room','Training Room'),('Big meeting room','Big meeting room'))
DURATION_CHOICE=(('30','30'),('60','60'))
EXTRA_CHOICE=(('0','0'),('2','2'),('3','3'))
NEED_CHOICE=(('Kitchen / Coffee','Kitchen / Coffee'),('Cleanness / Hygiene','Cleanness / Hygiene'),('Internet / WIFI','Internet / WIFI'),('Other','Other'))

class UserInfo(models.Model) :

    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    #fullName= models.CharField(max_length=25)
    #email = models.EmailField(max_length=254,unique=True,db_index=True)
    #password = models.CharField(max_length=70)
    #role= models.CharField(max_length=25)

    startup = models.CharField(max_length=50)
    profilePic = models.ImageField(upload_to='profile_pics',null=True)
    def __str__ (self):
        return self.user

class Reservation(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    space=models.CharField(max_length=100,choices=SPACE_CHOICE,default='B@Labs - Av. Habib Bourguiba')
    typeOf=models.CharField(max_length=100,default='Small meeting room')
    date = models.DateField(null=True, )
    startTime = models.TimeField(null=True, blank=True)
    endTime = models.TimeField(null=True,blank=True)
    duration = models.CharField(max_length=100,choices=DURATION_CHOICE,default='30')
    extraTime = models.CharField(max_length=100,choices=EXTRA_CHOICE,default='2hr')
    isValidated = models.BooleanField(default=True)
    notes = models.TextField(max_length=500,blank=True,null=True)
    def __str__ (self):
        return str(self.typeOf)


class Need(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product= models.CharField(max_length=200,choices=NEED_CHOICE,default="Kitchen / Coffee")
    notes= models.CharField(max_length=500)
    def __str__ (self):
        return str(self.product)


class Module(models.Model):
    number=models.IntegerField(blank=True,null=True)
    title=models.CharField(max_length=100)
    isActive=models.BooleanField(default=False)
    activationDate=models.DateField()
    def __str__ (self):
        return str(self.title)

class Course(models.Model):
    number=models.IntegerField(blank=True,null=True)
    title=models.CharField(max_length=100)
    isActive=models.BooleanField(default=False)
    module = models.ForeignKey(Module,on_delete=models.CASCADE)
    def __str__ (self):
        return str(self.id)


class Content(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE)
    videoURL=models.URLField(max_length=200,blank=True,null=True)
    articleURL=models.URLField(max_length=200,blank=True,null=True)
    textContent=models.TextField(blank=True,null=True)
    def __str__ (self):
        return str(self.course)
