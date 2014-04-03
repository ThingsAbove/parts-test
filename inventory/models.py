from django.db import models

# Create your models here.
DAY = 86400 # seconds in a day
    
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
        return int((timezone.now() - self.pub_date).total_seconds/DAYS)
