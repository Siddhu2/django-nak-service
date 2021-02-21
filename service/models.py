from django.db import models
from django.core.validators import RegexValidator
# Create your models here.

class service(models.Model):
    item = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    mobilenum = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    description = models.TextField(max_length=400)
    amount = models.CharField(max_length=100,null=True,blank=True, validators=[RegexValidator(r'^\d{1,10}$')])
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)

    def __str__(self):
        return self.customer
