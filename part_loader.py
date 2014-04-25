import csv
import sys
from inventory.models import Part,Supplier
import moneyed
from moneyed import Money,USD
from random import randint

supplier_names=(
    'Acme',
    'Best',
    'Rand',
)
with open(sys.argv[1], 'rb') as csvfile:
    partreader = csv.reader(csvfile, delimiter='|', quotechar='"')
    # Create missing suppliers
    for sup_name in supplier_names:
        if Supplier.objects.filter(name=sup_name).count() == 0:
            Supplier(name=sup_name).save()
            
    for row in partreader:
        #['name', 'supplier', 'description', 'cost', 'part_class']
        print row
        r_num = randint(1,10) #Inclusive
        s=Supplier.objects.get(name=row[1])
        pclass = row[4]
        print "Rand is:" + str(r_num)
        if r_num in range(1,6):
            pclass = 'C'            
            print "Class C"
        elif r_num in range(9,11):
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