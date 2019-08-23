from django.db import models


class Member(models.Model):
    phoneNumber = models.CharField(max_length=30)
    uid = models.CharField(max_length=60, unique=True)
    fcm_id = models.CharField(max_length=512)

    def __str__(self):
        return self.phoneNumber
