from inventory.models import Part,DemandLog
from random import randint
from datetime import timedelta, date
from django.utils import timezone

DAYS_OF_DEMAND = 90

part_list = Part.objects.all() #get parts
for p in part_list:
    
    now=timezone.now()    
    days_to_fill = DAYS_OF_DEMAND
    try:
        last_demand = DemandLog.objects.latest('time')
        days_to_fill = (now - last_demand.time).days
        print "Filling data for %(days)d days"%{'days': days_to_fill}
    except e:
        print "Problem getting last demandlog date" + e
        
    for d in range(days_to_fill,0,-1):
        t= now - timedelta(days=d)
        if t.weekday() in(5,6):
           continue # no weekends
        for h in range(12,22):
            p_num = randint(0,50) # get random number of demand
            if p.part_class in 'A':
                p_num = p_num / 10
            elif p.part_class in 'B':
                p_num = p_num / 3 
            mt = t + timedelta(hours=h,minutes=randint(0, 60))
            demand = DemandLog(part_type = p, time = mt, amount = (p_num / randint(1,3)))
            demand.save()