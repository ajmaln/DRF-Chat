from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
import datetime

from django.core.cache import cache



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handoff_to = models.CharField(max_length=100, default="", null=True) 
    # only required for handoff 
    api_sent = models.CharField(max_length=100, default="N", null=True) 
    
    def __str__(self):
        return self.user.username

    @property
    def get_handoff_to(self):
        return self.handoff_to

    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)
    
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else: 
            return False

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    

    class Meta:
        ordering = ('timestamp',)


