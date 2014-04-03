from django.contrib import admin

# Register your models here.
from inventory.models import Supplier,Part,Bin

class PartInline(admin.StackedInline):
    model = Part
    extra = 3
    
class SupplierAdmin(admin.ModelAdmin):
    fields = ['name', 'contact']
    inlines = [PartInline]    

admin.site.register(Part)
admin.site.register(Bin)
admin.site.register(SupplierAdmin)
