from django.conf.urls.defaults import *

from django.views.generic.list_detail import object_list
from django.views.generic.create_update import create_object

from universe.models import *

urlpatterns = patterns('',
	(r'^$', object_list,
		{'queryset':Constellation.objects.all(),}),
	(r'^star/$', 'universe.views.stars'),
	(r'^star/(?P<uuid>.+)/$', 'universe.views.star'),
	(r'^storage/(?P<uuid>.+)/$', 'universe.views.pool'),
)
