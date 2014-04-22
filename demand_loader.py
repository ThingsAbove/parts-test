from inventory.models import Part,DemandLog
from random import randint
from datetime import timedelta, date
from django.utils import timezone

SECS_IN_HOUR = 3600 # seconds in an hour
SECS_IN_DAY = 86400 # seconds in a day
HOURS_IN_DAY = 24
DAYS_OF_DEMAND = 90

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
    
    now=timezone.now()    
    for d in range(DAYS_OF_DEMAND,0,-1):
        t= now - timedelta(days=d)
        if t.weekday() in(5,6):
           continue # no weekends
        for h in range(8,18):
            p_num = randint(0,50) # get random number of demand
            if p.part_class in 'A':
                p_num = p_num / 10
            elif p.part_class in 'B':
                p_num = p_num / 3 
            mt = t + timedelta(hours=h,minutes=randint(0, 60))
            demand = DemandLog(part_type = p, time = mt, amount = (p_num / randint(1,3)))
            demand.save()