import django_tables2 as tables
from inventory.models import Part

class PartTable(tables.Table):
	class Meta:
		model = Part
		# add class="paleblue" to <table> tag
		attrs = {"class": "paleblue"}