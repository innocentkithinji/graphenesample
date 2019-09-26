from django.db import models
from Farm.models import Farm;
from Buyer.models import Buyer
from Sales.models import Sale


class Chat(models.Model):
    partyA = models.ForeignKey(Buyer, related_name="buyerChats", on_delete=models.CASCADE)
    partyB = models.ForeignKey(Farm, related_name="farmChats", on_delete=models.CASCADE)
    sale = models.ForeignKey(Sale, related_name="chats", on_delete=models.CASCADE, null=True)
    docId = models.TextField()

    def __str__(self):
        return self.docId
