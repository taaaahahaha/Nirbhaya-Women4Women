from django.db import models
from django.contrib.auth.models import User

class userProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    dob = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    

    def __str__(self):
        return f'{self.name}'


class SOS(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    mobile_number = models.CharField(max_length=200, blank=True, null=True)
    relation = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name
    