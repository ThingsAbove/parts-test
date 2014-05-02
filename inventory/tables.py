import django_tables2 as tables
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
import itertools
from inventory.models import Part, Bin, Supplier, Location

counter = itertools.count()


class PartTable(tables.Table):
	#name = tables.Column(verbose_name="part name")
	name = tables.TemplateColumn('<a href="/inventory/{{record.id}}">{{record.name}}</a>')
	edit = tables.TemplateColumn('<a href="/inventory/part/edit/{{record.id}}"><i class="glyphicon glyphicon-edit"></i></a>',verbose_name = ("Action"), orderable=False)
	class Meta:
		model = Part
		# add class="paleblue" to <table> tag
		sequence = ('name', 'edit', 'supplier','description',)
		exclude = ('id', 'cost_currency',)
		attrs = {"class": "table table-striped"}
		template = ('table.html')
		
class BinPartTable(tables.Table):
	#part_name = tables.TemplateColumn('<a href="/inventory/{{record.part_type.id}}">{{record.part_type.name}}</a>')
	part_name = tables.Column(accessor = 'part_type.name', verbose_name = ("Part Name"))
	part_supplier = tables.Column(accessor = 'part_type.supplier')
	part_description = tables.Column(accessor = 'part_type.description',orderable=False)
	part_safety_stock = tables.Column(accessor = 'part_type.safety_stock')
	part_cost = tables.Column(accessor = 'part_type.cost')
	count = tables.Column(verbose_name = ('In Stock'))
	class Meta:
		model = Bin
		# add class="paleblue" to <table> tag
		sequence = ('part_name','part_supplier','part_description', 'part_safety_stock', 'count')
		exclude = ('id', 'part_type','name','description','capacity',)
		attrs = {"class": "table table-striped"}
		template = ('table.html')

	def render_part_name(self, record):
	    	return mark_safe('''<a href="/inventory/%s">%s</a>''' % (record.part_type.id, record.part_type.name))
