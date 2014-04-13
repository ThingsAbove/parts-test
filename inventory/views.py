from django.shortcuts import render
from django.http import HttpResponse  
from django.template import RequestContext, loader
from inventory.models import Part

# Create your views here.

def index(request):
    parts_list = Part.objects.order_by('name')
    template = loader.get_template('inventory/index.html')
    context = RequestContext(request, {
        'parts_list': parts_list,
    })
    return HttpResponse(template.render(context))

def detail(request, inventory_id):
    return HttpResponse("You're looking at part_id %s." % inventory_id)

def results(request, inventory_id):
    return HttpResponse("You're looking at the results of inventory balance %s." % inventory_id)

def balance(request, inventory_id):
    return HttpResponse("You're balancing inventory %s." % inventory_id)