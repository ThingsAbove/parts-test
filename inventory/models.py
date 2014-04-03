from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime

# Create your models here.
SECS_IN_DAY = 86400 # seconds in a day
    
class Supplier(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name    
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)

class Part(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name      
    supplier = models.ForeignKey(Supplier)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
class Bin(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.location    
    part_type = models.ForeignKey(Part)
    capacity = models.IntegerField(default=100)
    count = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    replenish_date = models.DateTimeField('date replenished')
    def days_since_replenished(self):
        return int(((timezone.now() - self.replenish_date).total_seconds())/SECS_IN_DAY)
    def percent_remaining(self):
        if self.capacity:
            p = (float(self.count) / float(self.capacity)) * 100
            return ("%.0f" % p)
        else:
            return "NA"
    def clean(self):
        # Don't allow count to exceed capacity.
        if self.count > self.capacity:
            raise ValidationError('Count cannot exceed Capacity')
        # replenish_date cannot be in the future
        if self.replenish_date > datetime.date.today():
            raise ValidationError('Replenish date cannot be in the future')

