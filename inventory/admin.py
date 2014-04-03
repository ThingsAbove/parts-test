from django.contrib import admin

# Register your models here.
from inventory.models import Supplier,Part,Bin

admin.site.register(Supplier)
admin.site.register(Part)
admin.site.register(Bin)