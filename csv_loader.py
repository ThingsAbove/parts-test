import csv
from inventory.models import Part,Supplier
import moneyed
from moneyed import Money,USD

with open('/Users/ccarpenter/Downloads/dataApr-18-2014.csv', 'rb') as csvfile:
    partreader = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in partreader:
        #['name', 'supplier', 'description', 'cost', 'part_class']
        print row
        s=Supplier.objects.get(name=row[1])
        m=Money(row[3],'USD')
        p=Part(name=row[0], supplier=s, description=row[2], cost=m, part_class=row[4])
        p.save()