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
    name = models.CharField(max_length=200)
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

class Bin(models.Model):
    def __unicode__(self):  # Python 3: def __str__(self):
        return (self.location + ':' + str(self.part_type))
    part_type = models.ForeignKey(Part)
    capacity = models.IntegerField(default=100)
    count = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    replenish_date = models.DateTimeField('date replenished')
          
    def cost(self):
        if self.part_type:
            return (self.part_type.cost * self.count)
        else:
            return (Money(0,'USD'))
    
    def contains_part_class_category(self):
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

    def clean(self):
        # Don't allow count to exceed capacity.
        if self.count > self.capacity:
            raise ValidationError('Count cannot exceed Capacity')
        # replenish_date cannot be in the future
        if self.replenish_date > timezone.now():
            raise ValidationError('Replenish date cannot be in the future')

class Warehouse(models.Model):
    def __unicode__(self):
            return self.name
    name = models.CharField(max_length=200)
    bins = models.ManyToManyField(Bin)
    def number_of_bins(self):
        if bins:
            return bins.objects.count()
        else:
            return 0
    def number_of_part_class_a_bins(self):
        if bins:
            return (bins.objects.filter(bins__part_type__part_class=Part.PART_CLASS_A).count())
        else:
            return 0
    def number_of_part_class_b_bins(self):
        if bins:
            return (bins.objects.filter(bins__part_type__part_class=Part.PART_CLASS_B).count())
        else:
            return 0
    def number_of_part_class_c_bins(self):
        if bins:
            return (bins.objects.filter(bins__part_type__part_class=Part.PART_CLASS_C).count())
        else:
            return 0
    def total_cost(self):
        if bins:
            return (bins.objects.aggregate(Sum(part_type.cost)))
        else:
            return Money(0,'USD')