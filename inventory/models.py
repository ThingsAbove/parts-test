from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import moneyed
from djmoney.models.fields import MoneyField
from moneyed import Money, USD
from django.db.models import Count, Max, Avg, Sum

# Create your models here.
SECS_IN_DAY = 86400 # seconds in a day
    
class Supplier(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name    
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)

class Part(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return (self.name + ':class:' + self.part_class +':cost-per:' + str(self.cost))     
    supplier = models.ForeignKey(Supplier)
    name = models.CharField(max_length=200,verbose_name="Part Name")
    description = models.CharField(max_length=200)
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    PART_CLASS_A = 'A'
    PART_CLASS_B = 'B'
    PART_CLASS_C = 'C'
    PART_CLASS_UNKNOWN = 'U'
    PART_CLASS_CHOICES=(
        (PART_CLASS_A, 'very tight control and accurate records'),
        (PART_CLASS_B, 'less tightly controlled and good records'),
        (PART_CLASS_C, 'simplest controls possible and minimal records'),
        (PART_CLASS_UNKNOWN, 'not applicable or unknown'),
    )
    part_class = models.CharField(max_length=1, choices=PART_CLASS_CHOICES, default=PART_CLASS_C)

class DemandLog(models.Model):
    def __unicode__(self):
        return (str(self.time) + ':' + str(self.part_type) + ':' + str(self.amount))
    time = models.DateTimeField(default=timezone.now())
    part_type = models.ForeignKey(Part)
    amount = models.IntegerField(default=0)

class Location(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200, blank=True, null=True)
    
class Bin(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return (str(self.location.name) + ':' + str(self.part_type))
    part_type = models.ForeignKey(Part)
    capacity = models.IntegerField(default=100)
    count = models.IntegerField(default=0)
    location = models.ForeignKey(Location)
    replenish_date = models.DateTimeField('date replenished')
          
    def cost(self):
        if self.part_type:
            return (self.part_type.cost * self.count)
        else:
            return (Money(0,'USD'))
    
    def part_class_category_contents(self):
        if self.part_type:
            return (self.part_type.part_class)
        else:
            return Part.PART_CLASS_UNKNOWN
            
    def days_since_replenished(self):
        return int(((timezone.now() - self.replenish_date).total_seconds())/SECS_IN_DAY)

    def percent_remaining(self):
        if self.capacity:
            p = (float(self.count) / float(self.capacity)) * 100
            return ("%.0f" % p)
        else:
            return "NA"
    def pull(self, to_pull=1):
        if ((self.count - to_pull) >= 0):
            self.count = self.count - to_pull
            self.save()
            dl=DemandLog(time=timezone.now(), part_type=self.part_type, amount=to_pull)
            dl.save()
            return self.count
        else:
            return ValidationError('Cannot pull beyond empty')
    def clean(self):
        # Don't allow count to exceed capacity.
        if self.count > self.capacity:
            raise ValidationError('Count cannot exceed Capacity')
        # replenish_date cannot be in the future
        if self.replenish_date > timezone.now():
            raise ValidationError('Replenish date cannot be in the future')

class Facility(models.Model):
    def __unicode__(self):
            return self.name
    name = models.CharField(max_length=200)
    bins = models.ManyToManyField(Bin, through="BinOwnership")
    def number_of_bins(self):
        if self.bins:
            return self.bins.objects.count()
        else:
            return 0
            
class BinOwnership(models.Model):
    bin = models.ForeignKey(Bin)
    facility = models.ForeignKey(Facility)
    start_date = models.DateTimeField('Ownership start date')
    end_date = models.DateTimeField('Ownership end date', blank=True, null=True)
    def clean(self):
        # Don't allow end_date before start_date
        if self.end_date:
            if self.end_date < self.start_date:
                raise ValidationError('End date cannot preceed Start Date')
    
 