# Create your views here.

from universe.models import *

from django.http import HttpResponse
import csv

def star(request, uuid):
	s = Star.objects.get(uuid=uuid)

	if request.method == 'POST':
		s.hostname = request.POST.get('hostname', s.hostname)
		s.type = request.POST.get('type', s.type)
		s.model = request.POST.get('model', s.model)
		s.memory = request.POST.get('memory', s.memory)
		s.cpus = request.POST.get('cpus', s.cpus)
		s.mhz = request.POST.get('mhz', s.mhz)
		s.save()

	# finally, return current values (GET and POST)
	return_str = "%s,%s,%s,%s,%s,%s" % \
			(s.uuid, s.type, s.model, s.memory, s.cpus, s.mhz)

	response = HttpResponse(status=200, content=return_str)
	response['X-Honcheonui-Result'] = "OK"
	response['X-Honcheonui-Method'] = request.method
	response['Pragma'] = 'no-cache'

	return response

def stars(request):
	ss = Star.objects.all()

	response = HttpResponse(mimetype='text/csv')
	response['Content-Disposition'] = 'attachment; filename=stars.csv'

	writer = csv.writer(response)
	for s in ss:
		writer.writerow([s.uuid,s.uri,s.name,s.constellation])

	return response

def pool(request, uuid):
	try:
		p = Pool.objects.get(uuid=uuid)
	except:
		# create new pool with args
		p = Pool(uuid=uuid,name=name,capacity=capacity)

	return_str = "%s,%s,%s,%s" % \
			(p.name, p.type, p.path, p.capacity)

	response = HttpResponse(status=200, content=return_str)
	response['X-Honcheonui-Result'] = "OK"
	response['X-Honcheonui-Method'] = request.method
	response['Pragma'] = 'no-cache'

	return response


