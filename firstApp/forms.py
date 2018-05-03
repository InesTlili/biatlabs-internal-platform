from django import forms
from django.core import validators
from firstApp.models import UserInfo, Reservation, Need, Postit,Presence,Workshop,Evaluation,Objective
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta() :
        model = User
        fields=('username','email','password')

class ProfileForm(forms.ModelForm):
    class Meta():
        model = UserInfo
        fields=('startup',)

class reserve(forms.ModelForm):
    class Meta():
        model = Reservation
        fields=('typeOf','date','startTime','duration','extraTime')


    #name = forms.CharField(max_length=50)
    #email = forms.EmailField()
    #startup = forms.CharField(max_length=50)
    #password = forms.CharField(max_length=20, widget=forms.PasswordInput)
    #botcatcher = forms.CharField(required=False,widget=forms.HiddenInput,validators=[validators.MaxLengthValidator(0)])

class needform(forms.ModelForm):
    class Meta():
        model = Need
        fields = ('product','notes')
    #def cleanBotcatcher(self):
    #    botcatcher= self.cleaned_data['botcatcher']
    #    if len(botcatcher)>0 :
    #        raise forms.ValidationError("Gotchaaaa !!!")
    #        return botcatcher
class postitform(forms.ModelForm):
    class Meta():
        model = Postit
        fields = ('content',)


class presenceform(forms.ModelForm):
    class Meta():
        model = Presence
        fields = ('number','startup')

class addworkshop(forms.ModelForm):
    class Meta():
        model = Workshop
        fields = ('title','theme','otherTheme','date','time','duration','moderator',)

class evaluationform(forms.ModelForm):
        class Meta():
            model = Evaluation
            fields = ('founderMark','founderNotes','customerMark','customerNotes',
            'productMark','productNotes','teamMark','teamNotes','vpMark','vpNotes','financialMark',
            'financialNotes',)

class objectiveform(forms.ModelForm):
    class Meta():
        model = Objective
        fields = ('content',)

class PassForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('password',)
