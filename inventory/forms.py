# -*- coding: utf-8 -*-

from django.forms.models import ModelForm
from inventory.models import *

class PartForm(ModelForm):
	class Meta:
	    	model = Part
	    	fields = '__all__'
