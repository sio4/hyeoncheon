from django.db import models

import libvirt

# Create your models here.

class Constellation(models.Model):
	name = models.CharField(max_length=80)
	location = models.CharField(max_length=128)
	description = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name

STAR_STATUS_SEL = (
	('S', 'Stop'),
	('R', 'Run'),
)

STAR_MODE_SEL = (
	('C', 'Configured'),
	('I', 'Installed'),
	('D', 'Deployed'),
	('M', 'Maintenance'),
)

class Star(models.Model):
	name = models.CharField(max_length=80)
	url = models.CharField(max_length=128)

	is_virtual = models.BooleanField(default=False)
	deployed_on = models.ForeignKey('self', null=True,blank=True)

	status = models.CharField(max_length=1, choices=STAR_STATUS_SEL)
	mode = models.CharField(max_length=1, choices=STAR_MODE_SEL)

	constellation = models.ForeignKey(Constellation)

	def __unicode__(self):
		return self.name

	def listDomains(self):
		vms = []
		try:
			conn = libvirt.open(self.url)
			for id in conn.listDomainsID():
				dom = conn.lookupByID(id)
				vms.append(dom.name())
			conn.close()
		except:
			pass

		return vms

	def listDefinedDomains(self):
		try:
			conn = libvirt.open(self.url)
			vm_defined = conn.listDefinedDomains()
			conn.close()
		except:
			vm_defined = []

		return vm_defined

	def listNetworks(self):
		try:
			conn = libvirt.open(self.url)
			networks = conn.listNetworks()
			conn.close()
		except:
			networks = []

		return networks

	def listStoragePools(self):
		try:
			conn = libvirt.open(self.url)
			storage_pools = conn.listStoragePools()
			conn.close()
		except:
			storage_pools = []

		return storage_pools


	def getType(self):
		conn = libvirt.open(self.url)
		ret = conn.getType()
		conn.close()
		return ret

	def getInfo(self):
		conn = libvirt.open(self.url)
		ret = conn.getInfo()
		conn.close()
		return ret


	def get_vm_uuid_by_name(self, name):
		conn = libvirt.open(self.url)
		dom = conn.loolupByName(name)
		ret = dom.UUIDString()
		conn.close()
		return ret

	def get_vm_info_by_name(self, name):
		conn = libvirt.open(self.url)
		dom = conn.loolupByName(name)
		ret = dom.info()
		return ret


NETWORK_TYPE_SEL = (
	('I', 'Isolated'),
	('B', 'Bridged'),
	('N', 'NAT'),
)

class Network(models.Model):
	name = models.CharField(max_length=80)
	network = models.CharField(max_length=128)
	dhcp_start = models.IPAddressField()
	dhcp_end =models.IPAddressField()
	type =models.CharField(max_length=1, choices=NETWORK_TYPE_SEL)

	constellation = models.ForeignKey(Constellation)

	def __unicode__(self):
		return self.name

STORAGE_TYPE_SEL = (
	('D', 'Directory'),
	('B', 'Block Device'),
	('I', 'iSCSI'),
	('L', 'LVM'),
	('N', 'Network FS'),
)

class StoragePool(models.Model):
	name = models.CharField(max_length=80)
	type =models.CharField(max_length=1, choices=STORAGE_TYPE_SEL)
	path = models.CharField(max_length=128)

	hostname =models.CharField(max_length=128,null=True,blank=True)
	export = models.CharField(max_length=128,null=True,blank=True)

	constellation = models.ForeignKey(Constellation)

	def __unicode__(self):
		return self.name

