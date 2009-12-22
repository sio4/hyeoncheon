from django import template
from universe.models import *

register = template.Library()

@register.inclusion_tag('universe/template_list.html')
def template_list():
	templates = Volume.objects.filter(is_template=True)
	return {'templates':templates}


