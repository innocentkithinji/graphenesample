from django.db import models


class Member(models.Model):
    phoneNumber = models.CharField(max_length=20, unique=True)
    uid = models.CharField(max_length=60, unique=True)
    fcm_id = models.CharField(max_length=1024)

    def __str__(self):
        return self.phoneNumber
