from django.contrib import admin
from backend.models import *

# Register your models here.
admin.site.register([UserProfile, Event, UserRegisterEvent])