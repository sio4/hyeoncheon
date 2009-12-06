# Create your views here.
from django.http import HttpResponse


def trigger(request,id=0):

	string = "OK, Processed"
	result = "Processed"
	response = HttpResponse(status=200, content=string)
	response['X-Honcheonui-Result'] = result
	response['X-Honcheonui-Method'] = request.method
	response['Pragma'] = 'no-cache'

	return response
