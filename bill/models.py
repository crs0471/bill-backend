from django.db import models
from company.models import Company, Client

# Create your models here.
class Bill(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    note = models.TextField(max_length=200)
    description = models.TextField(max_length=200)
    due_date = models.DateField()
    cgst = models.FloatField()
    igst = models.FloatField()
    sgst = models.FloatField()
    discount = models.FloatField()
    shipping = models.FloatField()
    bill_no = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Bill_product(models.Model):
    bill = models.ForeignKey(to=Bill, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.FloatField()
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

class Bill_product_master(models.Model):
    company = models.ForeignKey(to=Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    code = models.CharField(max_length=100)

