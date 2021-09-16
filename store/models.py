from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    ip = models.CharField(max_length=300, null=True, blank=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    date_uploaded = models.DateTimeField('modified', auto_now=True, null=True, blank=True)
    def __str__(self):
        return str(self.name)