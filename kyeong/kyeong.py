#!/usr/bin/env python


import libvirt
import hcu


# basic (or global) variables


# setup startup environment. (or live configuration update)
stars = hcu.list_stars()

###
###
### function block -----------------------------------------------------------
def update_node_info(star):
	conn = libvirt.openReadOnly(star['uri'])
	hostname = conn.getHostname()
	type = conn.getType()
	ni = conn.getInfo()
	model = ni[0]
	memory = ni[1]
	cpus = ni[2]
	mhz = ni[3]

	s = hcu.update_star(star['uuid'],
			hostname, type, model, memory, cpus, mhz)
	print "star: %s, %s, %s, %sMB %scpus(%s MHz)" % \
			(s['uuid'], s['type'], s['model'],
					s['memory'], s['cpus'], s['mhz'])
	return conn

def update_volume_info(storage, name):
	volume = storage.storageVolLookupByName(name)
	path = volume.path()
	vi = volume.info()
	type = vi[0]
	capacity = vi[1]
	allocation = vi[2]

	print "  volume: %s, %s, %s, %s" % (name, type, capacity, allocation)
	print "   -- %s" % (path)
	return volume

def update_storage_info(star, name, volume_too=False):
	storage = star['conn'].storagePoolLookupByName(name)
	uuid = storage.UUIDString()
	si = storage.info()
	state = si[0]
	capacity = si[1]
	allocation = si[2]
	available = si[3]

	ret = hcu.update_pool(uuid,name,star,state,capacity,allocation,available)
	print ret

	print " pool: %s, %s, %sByte, %sByte, %sByte" % \
			(name, state, capacity, allocation, available)
	print "  -- %s" % (uuid)

	if volume_too == True:
		volume_names = storage.listVolumes()
		for vn in volume_names:
			update_volume_info(storage, vn)

	return storage

def update_network_info(conn, name):
	net = conn.networkLookupByName(name)
	bridge = net.bridgeName()
	uuid = net.UUIDString()

	print " net: %s %s %s" % (name, bridge, uuid)
	return net

def update_dom_info(conn, name):
	dom = conn.lookupByName(name)

	name = dom.name()
	uuid = dom.UUIDString()
	type = dom.OSType()

	di = dom.info()
	state = di[0]
	memory = di[2]
	cpus = di[3]
	cputime = di[4]

	print " vm: %s,%s,%s,%s,%s,%s,%s" % \
			(name, uuid, type, state, memory, cpus, cputime)
	return dom



###
###
### main routine	------------------------------------------------------

print "##########################"

for star in stars:
	star['conn'] = update_node_info(star)
	print star


for star in stars:
	conn = star['conn']

	storage_names = conn.listStoragePools()
	for pn in storage_names:
		storage = update_storage_info(star, pn)

		volume_names = storage.listVolumes()
		for vn in volume_names:
			update_volume_info(storage, vn)

	network_names = conn.listNetworks()
	for nn in network_names:
		net = update_network_info(conn, nn)

	domain_ids = conn.listDomainsID()
	for id in domain_ids:
		dom = conn.lookupByID(id)
		dom = update_dom_info(conn, dom.name())


	domain_names = conn.listDefinedDomains()
	for name in domain_names:
		dom = update_dom_info(conn, name)


for star in stars:
	star['conn'].close()
