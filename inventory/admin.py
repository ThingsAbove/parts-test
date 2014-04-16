from django.contrib import admin
import moneyed
from djmoney.models.fields import MoneyField

# Register your models here.
from inventory.models import Supplier,Part,Bin,Warehouse

class PartInline(admin.TabularInline):
    model = Part
    extra = 3
    
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'cost', 'part_class',)
      
class SupplierAdmin(admin.ModelAdmin):
    fields = ['name', 'contact']
    inlines = [PartInline]    
    
class BinAdmin(admin.ModelAdmin):
    fields = ['part_type','capacity','count','location','replenish_date']
    list_display = ('part_type', 'capacity','count','cost','percent_remaining', 'location', 'replenish_date', 'days_since_replenished',)
    list_filter = ['replenish_date']
    
class BinInline(admin.TabularInline):
	model=Warehouse.bins.through
	extra =3
	
class WarehouseAdmin(admin.ModelAdmin):
	fields = ('name',)
	inlines = [BinInline]

admin.site.register(Part, PartAdmin)
admin.site.register(Bin, BinAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Warehouse,WarehouseAdmin)

