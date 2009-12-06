# Create your views here.
from django.http import HttpResponse

from universe.models import *

import kyeong

def trigger(request,id=0):

	stars = Star.objects.all()
	for star in stars:
		conn = kyeong.update_node_info(star)
		kyeong.update_pool_info(conn, star)
		kyeong.update_network_info(conn, star)
		kyeong.update_dom_info(conn, star)

	string = "OK, Processed"
	result = "Processed"
	response = HttpResponse(status=200, content=string)
	response['X-Honcheonui-Result'] = result
	response['X-Honcheonui-Method'] = request.method
	response['Pragma'] = 'no-cache'

	return response
