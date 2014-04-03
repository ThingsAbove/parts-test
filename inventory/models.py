from django.db import models

# Create your models here.
    
class Supplier(models.Model):
    name = models.CharField(max_length=200)

class Part(models.Model):
    supplier = models.ForeignKey(Supplier)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    
class Bin(models.Model):
    part_type = models.ForeignKey(Part)
    capacity = models.IntegerField(default=100)
    count = models.IntegerField(default=0)
    location = models.CharField(max_length=200)
    replenish_date = models.DateTimeField('date replenished')