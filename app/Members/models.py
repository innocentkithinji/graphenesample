from django.db import models

from Agent.models import Agent

class Member(models.Model):
    phoneNumber = models.CharField(max_length=20, unique=True)
    uid = models.CharField(max_length=60, unique=True)
    fcm_id = models.CharField(max_length=1024)
    agent = models.ForeignKey(Agent, related_name="recruits", null=True, on_delete=models.SET_NULL)
    joined = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.phoneNumber
