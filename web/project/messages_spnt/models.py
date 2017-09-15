from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, related_name="messages_as_receiver")
    sender = models.ForeignKey(User, related_name="messages_as_sender")
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False, blank=True)