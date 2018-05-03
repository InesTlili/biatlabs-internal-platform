from django.db import models
from django.contrib.auth.models import User
# Create your models here.

SPACE_CHOICE=(('B@Labs - Av. Habib Bourguiba','B@Labs - Av. Habib Bourguiba'),)
TYPEOF_CHOICE=(('Small meeting room','Small meeting room'),('Training Room','Training Room'),('Big meeting room','Big meeting room'))
DURATION_CHOICE=(('30','30'),('60','60'))
EXTRA_CHOICE=(('0','0'),('2','2'),('3','3'))
NEED_CHOICE=(('Kitchen / Coffee','Kitchen / Coffee'),('Cleanness / Hygiene','Cleanness / Hygiene'),('Internet / WIFI','Internet / WIFI'),('Other','Other'))
THEME_CHOICE=(('Founder','Founder'),('Team','Team'),('Customer','Customer'),('Value Proposition','Value Proposition'),('Product','Product'),('Financial','Financial'))
THEMEDUR_CHOICE = (('1','1'),('2','2'),('3','3'))
MARK_CHOICE=(('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'))
WEEK_CHOICE=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10')
,('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'))

class Startup(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    industry = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    market = models.CharField(max_length=100)
    def __str__ (self):
        return str(self.name)
class UserInfo(models.Model) :

    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    #fullName= models.CharField(max_length=25)
    #email = models.EmailField(max_length=254,unique=True,db_index=True)
    #password = models.CharField(max_length=70)
    #role= models.CharField(max_length=25)

    startup = models.ForeignKey(Startup,on_delete=models.CASCADE)
    profilePic = models.ImageField(upload_to='profile_pics',null=True)
    def __str__ (self):
        return str(self.user)

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
    videoURL2=models.URLField(max_length=200,blank=True,null=True)
    videoURL3=models.URLField(max_length=200,blank=True,null=True)
    videoURL4=models.URLField(max_length=200,blank=True,null=True)
    videoURL5=models.URLField(max_length=200,blank=True,null=True)

    articleURL=models.URLField(max_length=200,blank=True,null=True)
    articleURL2=models.URLField(max_length=200,blank=True,null=True)
    articleURL3=models.URLField(max_length=200,blank=True,null=True)
    textContent=models.TextField(blank=True,null=True)
    def __str__ (self):
        return str(self.course)

class Locker(models.Model):
    reference=models.IntegerField(unique=True)
    Nearby=models.CharField(max_length=100,blank=True,null=True)
    isFree=models.BooleanField(default=True)
    adminValid=models.BooleanField(default=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    def __str__ (self):
        return str(self.isFree)

class Postit(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    content = models.CharField(max_length=100,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    def __str__ (self):
        return str(self.title)
class Visitor(models.Model):
    fullName=models.CharField(max_length=100)
    email=models.EmailField()
    visitedStartup=models.CharField(max_length=100)
    date = models.DateField(null=True,blank=True)
    timeIn = models.TimeField(null=True,blank=True)
    cinId=models.IntegerField(max_length=8,)



class Presence(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    number = models.IntegerField()
    def __str__ (self):
        return str(self.startup.name)


class Chair(models.Model):
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    d = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()
    v = models.IntegerField()
    w = models.IntegerField()

class Workshop(models.Model):
    title = models.CharField(max_length=100)
    theme = models.CharField(max_length=100,choices=THEME_CHOICE,default='Founder')
    otherTheme = models.CharField(max_length=100, null=True,blank=True)
    date = models.DateField()
    time = models.TimeField()
    duration = models.CharField(max_length=100,choices=THEMEDUR_CHOICE,default='1')
    moderator = models.CharField(max_length=100)
    isDone =models.BooleanField(default=False)
    startups = models.ManyToManyField(Startup, null=True, blank=True)
    def __str__ (self):
        return str(self.title)

class Evaluation(models.Model):
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    founderMark = models.IntegerField()
    founderNotes = models.CharField(max_length=500,null=True,blank=True)
    customerMark = models.IntegerField()
    customerNotes = models.CharField(max_length=500,null=True,blank=True)
    productMark = models.IntegerField()
    productNotes = models.CharField(max_length=500,null=True,blank=True)
    teamMark = models.IntegerField()
    teamNotes = models.CharField(max_length=500,null=True,blank=True)
    vpMark = models.IntegerField()
    vpNotes = models.CharField(max_length=500,null=True,blank=True)
    financialMark = models.IntegerField()
    financialNotes = models.CharField(max_length=500,null=True,blank=True)
    def __str__ (self):
        return str(self.startup.name)



class Week(models.Model):
    number=models.CharField(choices=SPACE_CHOICE,default='1',max_length=500)
    StartDate=models.DateField()
    EndDate=models.DateField()
    def __str__ (self):
        return str(self.id)

class WeeklyObj(models.Model):
    deadline=models.DateTimeField()
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    startup=models.ForeignKey(Startup, on_delete=models.CASCADE)
    def __str__ (self):
        return str(self.id)

class Objective(models.Model):
    content = models.CharField(max_length=1000)
    #week = models.CharField(choices=SPACE_CHOICE,default='1',max_length=500)
    #startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    isDone = models.BooleanField(default=False)
    wol=models.ForeignKey(WeeklyObj,on_delete=models.CASCADE)
    def __str__ (self):
        return str(self.id)
