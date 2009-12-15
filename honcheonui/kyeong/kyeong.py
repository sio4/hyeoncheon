#
# kyeong, libvirt driver module.
#

import libvirt


###
###
### function block -----------------------------------------------------------
def update_node_info(star):
	conn = libvirt.openReadOnly(star.uri)
	star.hostname = conn.getHostname()
	star.type = conn.getType()
	ni = conn.getInfo()
	star.model = ni[0]
	star.memory = ni[1]
	star.cpus = ni[2]
	star.mhz = ni[3]

	star.save()

	return conn


def update_pool_info(conn, star):
	virt_pools = conn.listStoragePools()
	for name in virt_pools:
		virt_pool = conn.storagePoolLookupByName(name)
		uuid = virt_pool.UUIDString()
		pi = virt_pool.info()
		state = str(pi[0])
		capacity = pi[1] / 1048576
		allocation = pi[2] / 1048576
		available = pi[3] / 1048576

		p = star.constellation.pool_set.get_or_create(uuid=uuid)[0]
		p.name = name
		p.capacity = capacity
		p.save()
		p.poolstatus_set.get_or_create(state=state,
				allocation=allocation, available=available)
		pl = star.poollink_set.get_or_create(pool=p, star=star)[0]

		update_volume_info(conn, virt_pool, star, p)

	return conn.numOfStoragePools()


def update_volume_info(conn, virt_pool, star, pool):
	virt_vols = virt_pool.listVolumes()
	for name in virt_vols:
		virt_volume = virt_pool.storageVolLookupByName(name)
		path = virt_volume.path()
		vi = virt_volume.info()
		type = vi[0]
		capacity = vi[1] / 1048576
		allocation = vi[2] / 1048576
		uuid = name.split('.')[0]

		v = pool.volume_set.get_or_create(uuid=uuid)[0]
		v.type = type
		v.path = path
		v.capacity = capacity
		v.save()
		v.volumestatus_set.get_or_create(allocation=allocation)
		v.volumelink_set.get_or_create(star=star)

	return True


def update_network_info(conn, star):
	for name in conn.listNetworks():
		net = conn.networkLookupByName(name)
		bridge = net.bridgeName()
		uuid = net.UUIDString()

		n = star.constellation.network_set.get_or_create(uuid=uuid)[0]
		n.name = name
		n.bridge = bridge
		n.save()

	return conn.numOfNetworks()


def update_dom_info(conn, star):
	doms = conn.listDefinedDomains()
	for id in conn.listDomainsID():
		doms.append(conn.lookupByID(id).name())

	for name in doms:
		dom = conn.lookupByName(name)
		uuid = dom.UUIDString()
		di = dom.info()
		state = str(di[0])
		memory = di[2]
		cpus = di[3]
		cputime = di[4] / 1000000000	# nano

		light = star.constellation.light_set.get_or_create(uuid=uuid)[0]
		light.name = dom.name()
		light.type = dom.OSType()
		light.memory = memory
		light.cpus = cpus
		light.save()

		light.lightstatus_set.get_or_create(star=star,
				state=state, cputime=cputime)

	return conn.numOfDefinedDomains() + conn.numOfDomains()

