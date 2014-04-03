from django.shortcuts import render
from django.http import HttpResponse  

# Create your views here.

def index(request):
    return HttpResponse("You're at the inventory index.")

def detail(request, inventory_id):
    return HttpResponse("You're looking at inventory %s." % inventory_id)

def results(request, inventory_id):
    return HttpResponse("You're looking at the results of inventory balance %s." % inventory_id)

def balance(request, inventory_id):
    return HttpResponse("You're balancing inventory %s." % inventory_id)