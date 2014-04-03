from django.contrib import admin

# Register your models here.
from inventory.models import Supplier,Part,Bin

class PartInline(admin.TabularInline):
    model = Part
    extra = 3
    
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    
class SupplierAdmin(admin.ModelAdmin):
    fields = ['name', 'contact']
    inlines = [PartInline]    
    
class BinAdmin(admin.ModelAdmin):
    fields = ['part_type','capacity','count','location','replenish_date']
    list_display = ('part_type', 'capacity','count', 'percent_remaining', 'location', 'replenish_date', 'days_since_replenished')
    list_filter = ['replenish_date']

admin.site.register(Part, PartAdmin)
admin.site.register(Bin, BinAdmin)
admin.site.register(Supplier, SupplierAdmin)
