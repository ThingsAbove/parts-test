from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django_tables2   import RequestConfig
from inventory.models import Part
from inventory.tables import PartTable

# Create your views here.
ITEMS_PER_PAGE=10


def index(request):
    table = PartTable(Part.objects.all().order_by('name'))
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/index.html', {'table': table})
    
def all_parts(request):
    table = PartTable(Part.objects.all().order_by('name'))
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/index.html', {'table': table})
    
def parts_by_class(request, part_class):
    table = PartTable(Part.objects.filter(part_class=part_class).order_by('name'))
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/index.html', {'table': table})
    
def detail(request, inventory_id):
    part = get_object_or_404(Part, pk=inventory_id)
    return render(request, 'inventory/detail.html', {'part': part})

def results(request, inventory_id):
    return HttpResponse("You're looking at the results of inventory balance %s." % inventory_id)

def balance(request, inventory_id):
    return HttpResponse("You're balancing inventory %s." % inventory_id)
    
