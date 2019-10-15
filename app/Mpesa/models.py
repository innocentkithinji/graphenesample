from django.db import models


# Create your models here.
class payRequest(models.Model):
    phone = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    amount = models.CharField(max_length=40)
    checkOutID = models.CharField(max_length=100, blank=True)
    posted = models.BooleanField()


# {'TransactionType': '', 'TransID': 'NJ551HAKRP', 'TransTime': '20191005161329', 'TransAmount': '300.00',
#  'BusinessShortCode': '600755', 'BillRefNumber': 'BY6543211', 'InvoiceNumber': '', 'OrgAccountBalance': '',
#  'ThirdPartyTransID': '', 'MSISDN': '254708374149', 'FirstName': 'John', 'MiddleName': 'J.', 'LastName': 'Doe'}
class paymentMade(models.Model):
    transactionID = models.CharField(max_length=30)
    time = models.CharField(max_length=40)
    transAmount = models.IntegerField()
    accountRef = models.CharField(max_length=40)
    phone = models.CharField(max_length=40)
    payer = models.CharField(max_length=100)

    def __str__(self):
        return f"Transaction ID: {self.transactionID} Phone: {self.phone}"
