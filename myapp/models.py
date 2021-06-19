from django.db import models
import datetime 
import pytz 
current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
class Message(models.Model):
    content = models.TextField()
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    receiver = models.CharField(max_length=255,default="")
    receivertype = models.CharField(max_length=100,default="patient")
    msgread = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default="offline")
    last_seen = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date_added',)


class Receiver(models.Model):
    senderuser = models.CharField(max_length=255)
    receiveruser = models.CharField(max_length=255)
    msgread = models.BooleanField(default=False)
    status = models.CharField(max_length=20,default="offline")

    def __str__(self):
        return super().__str__()