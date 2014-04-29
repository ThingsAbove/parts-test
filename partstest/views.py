from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django_tables2   import RequestConfig



def about(request):
    return render(request,'about.html')
        
def contact(request):
    return render(request,'contact.html')