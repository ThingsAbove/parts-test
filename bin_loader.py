from inventory.models import Part,Supplier,Bin,Location
import moneyed
from moneyed import Money,USD
from random import randint
from datetime import timedelta, date
from django.utils import timezone

SECS_IN_DAY = 86400 # seconds in a day
location_names=(
    'Final assembly',
    'Workspace 3',
    'Stock aisle 2',
    'Stock aisle 1',
    'Stock Aisle 3',
    'Workspace 2',
    'Workspace 1',
)
part_list = Part.objects.all() #get parts
for p in part_list:
    p_num = randint(100,1000) # get random number of parts for bin
    l_num = randint(0,6) # choose a location at random
    l = Location.objects.get(name=location_names[l_num])
    
    if p.part_class in 'A':
        p_num = p_num / 10
    elif p.part_class in 'B':
        p_num = p_num / 3
        l_num = l_num * 3
    else:
        l_num = l_num * 10
        
    cp = p_num
    ct = p_num - l_num # show some usage
    
    t=timezone.now()
    rd = t - timedelta(days=randint(1, 90))
    b = Bin(part_type=p,location=l,count=ct,capacity=cp,replenish_date=rd)
    b.save()

    
