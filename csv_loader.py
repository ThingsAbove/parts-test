import csv
from inventory.models import Part,Supplier
import moneyed
from moneyed import Money,USD
from random import randint

with open('/Users/ccarpenter/Downloads/dataApr-18-2014.csv', 'rb') as csvfile:
    partreader = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in partreader:
        #['name', 'supplier', 'description', 'cost', 'part_class']
        print row
        r_num = randint(1,10) #Inclusive
        s=Supplier.objects.get(name=row[1])
        pclass = row[4]
        print "Rand is:" + str(r_num)
        if r_num <= 7:
            pclass = 'C'            
            print "Class C"
        elif r_num == 10:
            plcass = 'A'
            print "Class A"
        else:
            pclass = 'B'
            print "Class B"
            
        m=float(row[3])
        if pclass in 'C':
            m = m * 0.03
        elif pclass in 'B':
            m = m * 0.5
        else:
            m = m * 2
        m=Money(str(m),'USD')
        print m
        p=Part(name=row[0], supplier=s, description=row[2], cost=m, part_class=pclass)
        p.save()