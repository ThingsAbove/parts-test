from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import RequestContext
from django.db.models import F, Sum
from django_tables2   import RequestConfig
from inventory.models import Part, Bin, DemandLog
from inventory.tables import PartTable, BinPartTable, Supplier, Location
from inventory.forms import PartForm
from django import forms
from ajax_select.fields import AutoCompleteField

import datetime, time


# Create your views here.
ITEMS_PER_PAGE=20

def home(request):
    xdata = ['Class-A Parts','Class-B Parts','Class-C Parts']
    a_count = Part.objects.filter(part_class=Part.PART_CLASS_A).count()
    b_count = Part.objects.filter(part_class=Part.PART_CLASS_B).count()
    c_count = Part.objects.filter(part_class=Part.PART_CLASS_C).count()
    ydata = [a_count, b_count, c_count]
    chartdata = {'x':xdata, 'y':ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'chart_title': 'Parts by Class',
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    data['total_num_parts']=Part.objects.all().count()
    bins= Bin.objects.filter(part_type__safety_stock__gte=F('count')) # Select bins with count below part safety stock
    data['num_parts_below_safety_stock']=bins.count()
    table = BinPartTable(bins)
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    data['table']=table
    data['all_parts_count']=Bin.objects.aggregate(Sum('count'))['count__sum']
    data['num_suppliers']=Supplier.objects.all().count()
    data['oldest_replenished_bin']=Bin.objects.all().earliest('replenish_date')
    data['total_bins']=Bin.objects.all().count()
    return render(request,'inventory/home.html', data)
        
def parts_list(request):
    # Retrieve 
    parts = Part.objects.all().order_by('name')
    table = PartTable(parts)
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/parts_list.html', {'table': table})
    
def all_parts(request):
    table = PartTable(Part.objects.all().order_by('name'))
    xdata = ['Class-A Parts','Class-B Parts','Class-C Parts']
    a_count = Part.objects.filter(part_class=Part.PART_CLASS_A).count()
    b_count = Part.objects.filter(part_class=Part.PART_CLASS_B).count()
    c_count = Part.objects.filter(part_class=Part.PART_CLASS_C).count()
    ydata = [a_count, b_count, c_count]
    chartdata = {'x':xdata, 'y':ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)    
    data['table']=table
    return render(request, 'inventory/home.html', data)
    
def parts_by_class(request, part_class):
    table = PartTable(Part.objects.filter(part_class=part_class).order_by('name'))
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/home.html', {'table': table})

        
def detail(request, inventory_id):
    part = get_object_or_404(Part, pk=inventory_id) 
    # Determine the last valid demand log entry
    dl=DemandLog.objects.filter(part_type = part).latest('time')
    end_date = dl.time
    start_date = dl.time - datetime.timedelta(days=5) # show last x-days of logs
    part_name = part.name
    queryset = DemandLog.objects.filter(time__range=(start_date,end_date),part_type = part)
    
    data_source=[]
    for d in queryset:
        data_source.append([turn_ts_to_jsts(d.time), d.amount])
    
    data = {'data_source': data_source}
    data['part_name'] =  part_name
    data['start_date']= turn_ts_to_jsts(start_date)
    data['end_date']= turn_ts_to_jsts(end_date)
    data['txt_start_date']=start_date
    data['txt_end_date']=end_date
    data['part']= part
    data['bins']= Bin.objects.filter(part_type=part)
    
    return render(request,'inventory/detail.html', data)
    
def results(request, inventory_id):
    return HttpResponse("You're looking at the results of inventory balance %s." % inventory_id)

def balance(request, inventory_id):
    return HttpResponse("You're balancing inventory %s." % inventory_id)
    
def piechart(request):
    xdata = ['Class-A Parts','Class-B Parts','Class-C Parts']
    a_count = Part.objects.filter(part_class=Part.PART_CLASS_A).count()
    b_count = Part.objects.filter(part_class=Part.PART_CLASS_B).count()
    c_count = Part.objects.filter(part_class=Part.PART_CLASS_C).count()
    ydata = [a_count, b_count, c_count]
    chartdata = {'x':xdata, 'y':ydata}
    charttype = "pieChart"
    chartcontainer = 'piechart_container'
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'chart_title': 'Parts by Class',
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    return render(request,'inventory/nvdchart.html', data)
    
def barchart(request):
    xdata = ['Class-A Parts','Class-B Parts','Class-C Parts']
    a_count = Part.objects.filter(part_class=Part.PART_CLASS_A).count()
    b_count = Part.objects.filter(part_class=Part.PART_CLASS_B).count()
    c_count = Part.objects.filter(part_class=Part.PART_CLASS_C).count()
    ydata = [a_count, b_count, c_count]
    chartdata = {'x':xdata, 'y':ydata}
    charttype = "discreteBarChart"
    chartcontainer = 'discreteBarChart'
    data = {
        'chart_title': 'Parts by Class',
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
        }
    }
    extra_serie = {"tooltip": {"y_start": "There are ", "y_end": " calls"}}
    return render(request,'inventory/nvdchart.html', data)

def turn_ts_to_jsts(ts): # Turn a timestamp into a Javascript timestamp
    return (time.mktime(ts.timetuple()) *1000) 
    
def linechart(request, inventory_id):
    part = get_object_or_404(Part, pk=inventory_id) 
    # Determine the last valid demand log entry
    dl=DemandLog.objects.filter(part_type = part).latest('time')
    end_date = dl.time
    start_date = dl.time - datetime.timedelta(days=5) # show last x-days of logs
    part_name = part.name
    queryset = DemandLog.objects.filter(time__range=(start_date,end_date),part_type = part)
    
    data_source=[]
    for d in queryset:
        data_source.append([turn_ts_to_jsts(d.time), d.amount])

    data = {'data_source': data_source}
    data['part_name'] =  part_name
    data['start_date']= turn_ts_to_jsts(start_date)
    data['end_date']= turn_ts_to_jsts(end_date)

    return render(request,'inventory/linechart.html', data)
    
@login_required(login_url="/inventory/login")
def edit_part(request, id=None):
    form_args = {}
    part = get_object_or_404(Part, pk=id) 
    # else create new Part...        

    if request.POST:
        part_form = PartForm(request.POST, instance = part)
        if part_form.is_valid():
            part = part_form.save(commit=True)
    else:
        part_form = PartForm(instance = part)

    return render_to_response('inventory/part.html',
        {
            'part_form': part_form
        },
        context_instance=RequestContext(request)
    )