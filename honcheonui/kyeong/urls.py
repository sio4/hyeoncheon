from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^trigger/$', 'kyeong.views.trigger'),
)
