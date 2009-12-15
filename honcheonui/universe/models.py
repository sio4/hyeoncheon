from django.db import models

import libvirt
import uuid

###
### helper functions

def make_uuid():
	return str(uuid.uuid4())


###
### logical classes

### constellation
class Constellation(models.Model):
	uuid = models.CharField(max_length=36,default=make_uuid,editable=False)
	name = models.CharField(max_length=80)
	location = models.CharField(max_length=128)
	description = models.CharField(max_length=256, null=True,blank=True)

	version = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name


###
### represent physical part of cluster.

### physical machine
STAR_STATUS_SEL = (
	('r', 'running'),
	('s', 'shutoff'),
)

STAR_MODE_SEL = (
	('c', 'configured'),
	('i', 'installed'),
	('d', 'deployed'),
	('m', 'maintenance'),
)

class Star(models.Model):
	uuid = models.CharField(max_length=36,default=make_uuid,editable=False)
	name = models.CharField(max_length=80)
	uri = models.CharField(max_length=128)

	constellation = models.ForeignKey(Constellation)
	version = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

	## libvirt structure
	hostname = models.CharField(max_length=80,null=True,blank=True)
	type = models.CharField(max_length=20,null=True,blank=True)
	model = models.CharField(max_length=32,null=True,blank=True)
	memory = models.IntegerField(default=0)
	cpus = models.IntegerField(default=0)
	mhz = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class StarStatus(models.Model):
	status = models.CharField(max_length=1, choices=STAR_STATUS_SEL)
	mode = models.CharField(max_length=1, choices=STAR_MODE_SEL)
	class Meta:
		get_latest_by = 'timestamp'


### virtual machine
DOM_STATE_SEL = (
	('0', 'no state'),
	('1', 'running'),
	('2', 'blocked'),
	('3', 'paused'),
	('4', 'shutdown'),
	('5', 'shutoff'),
	('6', 'crashed'),
)

class Light(models.Model):
	uuid = models.CharField(max_length=36)
	name = models.CharField(max_length=80)

	constellation = models.ForeignKey(Constellation)
	version = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

	# is it config or libvirt-info?
	type = models.CharField(max_length=20)
	memory = models.IntegerField(default=0)
	cpus = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class LightStatus(models.Model):
	state = models.CharField(max_length=1,choices=DOM_STATE_SEL)
	cputime = models.PositiveIntegerField(default=0)

	star = models.ForeignKey(Star, null=True, blank=True)

	light = models.ForeignKey(Light)
	timestamp = models.DateTimeField(auto_now=True)
	class Meta:
		get_latest_by = 'timestamp'


### network (virtual or physical)
NETWORK_TYPE_SEL = (
	('I', 'Isolated'),
	('B', 'Bridged'),
	('N', 'NAT'),
)

class Network(models.Model):
	uuid = models.CharField(max_length=36)
	name = models.CharField(max_length=80)
	network = models.CharField(max_length=128,null=True,blank=True)
	dhcp_start = models.IPAddressField(null=True,blank=True)
	dhcp_end =models.IPAddressField(null=True,blank=True)
	type =models.CharField(max_length=1, choices=NETWORK_TYPE_SEL)

	constellation = models.ForeignKey(Constellation)
	version = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

	# is it related on libvirt? global or local?
	bridge = models.CharField(max_length=80)

	def __unicode__(self):
		return self.name


### storage pool
STORAGE_TYPE_SEL = (
	('d', 'directory'),
	('b', 'block device'),
	('i', 'iscsi'),
	('l', 'lvm'),
	('n', 'network fs'),
)

STORAGE_STATE_SEL = (
	('0', 'inactive'),
	('1', 'building'),
	('2', 'running'),
	('3', 'degraded'),
)

class Pool(models.Model):
	uuid = models.CharField(max_length=36)
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1,default='d',
			choices=STORAGE_TYPE_SEL)
	path = models.CharField(max_length=128,null=True,blank=True)
	is_shared = models.BooleanField(default=False)

	hostname =models.CharField(max_length=128,null=True,blank=True)
	export = models.CharField(max_length=128,null=True,blank=True)

	constellation = models.ForeignKey(Constellation)
	version = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

	capacity = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class PoolStatus(models.Model):
	state = models.CharField(max_length=1, choices=STORAGE_STATE_SEL)
	allocation = models.IntegerField(default=0)
	available = models.IntegerField(default=0)

	pool = models.ForeignKey(Pool)
	timestamp = models.DateTimeField(auto_now=True)
	class Meta:
		get_latest_by = 'timestamp'

class PoolLink(models.Model):
	pool = models.ForeignKey(Pool)
	star = models.ForeignKey(Star)


### storage volume
VOLUME_TYPE_SEL = (
	('0', 'file'),
	('1', 'block'),
)

class Volume(models.Model):
	uuid = models.CharField(max_length=36)
	name = models.CharField(max_length=80,default='Untitled')
	type = models.CharField(max_length=1,choices=VOLUME_TYPE_SEL)

	# from libvirt?
	path = models.CharField(max_length=265)
	capacity = models.IntegerField(default=0)

	light = models.ForeignKey(Light,null=True,blank=True)
	is_template = models.BooleanField(default=False)
	parent = models.ForeignKey('self',null=True,blank=True)

	pool = models.ForeignKey(Pool)
	version = models.IntegerField(default=0)
	timestamp = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

class VolumeStatus(models.Model):
	allocation = models.IntegerField(default=0)

	volume = models.ForeignKey(Volume)
	timestamp = models.DateTimeField(auto_now=True)
	class Meta:
		get_latest_by = 'timestamp'

class VolumeLink(models.Model):
	volume = models.ForeignKey(Volume)
	star = models.ForeignKey(Star)


#### TODO: add version information

