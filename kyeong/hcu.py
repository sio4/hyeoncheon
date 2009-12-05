#
#
#

import httplib, urllib
import sys


# statics
version = "0.1"
program = "hcu_comm"
python_version = "python/%s" % (sys.version.split()[0])

# how can i use configuration file?
server = '211.115.15.31:6244'


def _get(server, path):
	agent_str = "%s/%s (%s)" % (program, version, python_version)
	headers = { 'User-Agent':agent_str, }
	conn = httplib.HTTPConnection(server)
	conn.request("GET", path)
	response = conn.getresponse()
	data = response.read()
	conn.close()

	ret = {'status':response.status, 'data':data}
	return ret

def _post(server, path, params):
	agent_str = "%s/%s (%s)" % (program, version, python_version)
	headers = {
			'Content-Type':'application/x-www-form-urlencoded',
			'User-Agent':agent_str,
	}
	conn = httplib.HTTPConnection(server)
	conn.request("POST", path, params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()

	ret = {'status':response.status, 'data':data}
	return ret


def list_stars():
	path = '/universe/star/'
	ret = _get(server, path)
	tmp = ret['data'].split()
	stars = []
	for t in tmp:
		s = t.split(',')
		star = {'uuid':s[0],'uri':s[1],'name':s[2],'constellation':s[3]}
		stars.append(star)
	return stars


def update_star(uuid,hostname,type,model,memory,cpus,mhz):
	path = '/universe/star/%s/' % (uuid)
	params = urllib.urlencode({
		'hostname':hostname,
		'type':type,
		'model':model,
		'memory':memory,
		'cpus':cpus,
		'mhz':mhz,
	})
	ret = _post(server, path, params)
	s = ret['data'].split(',')
	star_info = {'uuid':s[0],'type':s[1],'model':s[2],
			'memory':s[3],'cpus':s[4],'mhz':s[5]}
	return star_info

def update_pool(uuid,name,star,state,capacity,allocation,available):
	path = '/universe/storage/%s/' % (uuid)
	params = urllib.urlencode({
		'name':name,
		'star':star['name'],
		'constellation':star['constellation'],
		'state':state,
		'capacity':capacity,
		'allocation':allocation,
		'available':available,
	})
	ret = _post(server, path, params)
	return ret









