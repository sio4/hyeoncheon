from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object

from main.models import ServiceInstance,ServiceItem

urlpatterns = patterns('',
	(r'^services/$', object_list,
		{'queryset':ServiceInstance.objects.all(),}),
	(r'^serviceitems/$', object_list,
		{'queryset':ServiceItem.objects.all(),}),
)
