from django.db import models

# Create your models here.

class Safespaces(models.Model):

    name = models.CharField(max_length=200, blank=True, null=True)
    distance = models.CharField(max_length=200, blank=True, null=True)
    rush = models.CharField(max_length=200, blank=True, null=True)
    availability = models.CharField(max_length=200, blank=True, null=True)
    score = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name