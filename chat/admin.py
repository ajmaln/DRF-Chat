from django.contrib import admin
from chat.models import Message, UserProfile

# Register your models here.
admin.site.register(Message)
admin.site.register(UserProfile)
