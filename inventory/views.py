from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django_tables2   import RequestConfig
from inventory.models import Part, Bin, DemandLog
from inventory.tables import PartTable
import datetime, time
from datetime import timedelta
from django.utils import timezone


# Create your views here.
ITEMS_PER_PAGE=10


def index(request):
    table = PartTable(Part.objects.all().order_by('name'))
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/index.html', {'table': table})
    
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
    return render(request, 'inventory/index.html', data)
    
def parts_by_class(request, part_class):
    table = PartTable(Part.objects.filter(part_class=part_class).order_by('name'))
    RequestConfig(request,paginate={"per_page": ITEMS_PER_PAGE}).configure(table)
    return render(request, 'inventory/index.html', {'table': table})
    
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
    