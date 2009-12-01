#!/usr/bin/env python


import libvirt


# basic (or global) variables
stars = []



# setup startup environment. (or live configuration update)

stars.append({'uri':'qemu+ssh://vios@50.1.102.192:2022/system'})
stars.append({'uri':'qemu+ssh://vios@50.1.102.194/system'})


print ""

for star in stars:
	star['uri']
	star['conn'] = libvirt.openReadOnly(star['uri'])

	conn = star['conn']

	hostname = conn.getHostname()
	type = conn.getType()

	ni = conn.getInfo()
	model = ni[0]
	memory = ni[1]
	cpus = ni[2]
	mhz = ni[3]

	print "\nstar: %s, %s, %s, %sMB %scpus(%s MHz)" % \
			(hostname, type, model, memory, cpus, mhz)

	storage_names = conn.listStoragePools()
	for pn in storage_names:
		storage = conn.storagePoolLookupByName(pn)
		p_uuid = storage.UUIDString()
		si = storage.info()
		state = si[0]
		capacity = si[1]
		allocation = si[2]
		available = si[3]

		print " pool: %s, %s, %sByte, %sByte, %sByte" % \
				(pn, state, capacity, allocation, available)
		print "  -- %s" % (p_uuid)

		volume_names = storage.listVolumes()
		for vn in volume_names:
			volume = storage.storageVolLookupByName(vn)
			vi = volume.info()
			path = volume.path()
			type = vi[0]
			capacity = vi[1]
			allocation = vi[2]

			print "  volume: %s, %s, %s, %s" % \
					(vn, type, capacity, allocation)
			print "   -- %s" % (path)

	network_names = conn.listNetworks()
	for nn in network_names:
		net = conn.networkLookupByName(nn)
		bridge = net.bridgeName()
		uuid = net.UUIDString()

		print " net: %s %s %s" % (nn, bridge, uuid)

	domain_ids = conn.listDomainsID()
	for id in domain_ids:
		dom = conn.lookupByID(id)
		print " vm: %s, %s" % (dom.name(), dom.info())


	domain_names = conn.listDefinedDomains()
	for name in domain_names:
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




for star in stars:
	star['conn'].close()
