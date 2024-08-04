from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=256) # this max length bit is a kwarg
    date = models.CharField(max_length=256) 
    location = models.CharField(max_length=256)
    description = models.TextField(max_length=256)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'event_id': self.id})