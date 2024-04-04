from django.contrib import admin
from .models import UserProfile,Participant,VideoCall

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(VideoCall)
admin.site.register(Participant)