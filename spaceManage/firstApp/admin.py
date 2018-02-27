from django.contrib import admin
from firstApp.models import UserInfo, Reservation, Need,Module,Course,Content
# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Reservation)
admin.site.register(Need)
admin.site.register(Module)
admin.site.register(Course)
admin.site.register(Content)
