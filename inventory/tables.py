import django_tables2 as tables
import itertools
from inventory.models import Part

counter = itertools.count()


class PartTable(tables.Table):
	#name = tables.Column(verbose_name="part name")
	name = tables.TemplateColumn('<a href="/inventory/{{record.id}}">{{record.name}}</a>')
	description = tables.Column(orderable=False)
	class Meta:
		model = Part
		# add class="paleblue" to <table> tag
		sequence = ('name','supplier','description',)
		exclude = ('id', 'cost_currency',)
		attrs = {"class": "table table-striped"}
		template = ('table.html')