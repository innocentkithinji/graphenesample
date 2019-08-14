from django.db import models


class Member(models.Model):
    phoneNumber = models.CharField(max_length=12)
    uid = models.CharField(max_length=60)
    fcm_id = models.CharField(max_length=70)

    def __str__(self):
        return self.phoneNumber
