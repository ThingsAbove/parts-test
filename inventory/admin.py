from django.contrib import admin

# Register your models here.
from inventory.models import Supplier,Part,Bin

class PartInline(admin.TabularInline):
    model = Part
    extra = 3
    
class SupplierAdmin(admin.ModelAdmin):
    fields = ['name', 'contact']
    inlines = [PartInline]    
    
class BinAdmin(admin.ModelAdmin):
    fields = ['part_type','capacity','count','location','replenish_date']

admin.site.register(Part)
admin.site.register(Bin, BinAdmin)
admin.site.register(Supplier, SupplierAdmin)
