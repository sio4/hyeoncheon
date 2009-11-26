from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TYPE_SEL = (
	('M', 'Virtual Machine'),
	('S', 'Storage'),
)

STATUS_SEL = (
	('N', 'New'),
	('A', 'Active'),
	('R', 'Running'),
	('S', 'Suspended'),
	('E', 'Expired'),
)

SOURCE_SEL = (
	('S', 'Standard'),
	('T', 'Third Party'),
	('B', 'Backup'),
	('C', 'Custom'),
)

IMAGE_TYPE_SEL = (
	('F', 'Image File'),
	('L', 'LVM Volume'),
	('R', 'Raw Partition'),
)

RELEASE_STATUS_SEL = (
	('D', 'Draft'),
	('R', 'Released'),
	('P', 'Postponed'),
	('E', 'Expired'),
)


class ServiceItem(models.Model):
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1, choices=TYPE_SEL)

	status = models.CharField(max_length=1, choices=RELEASE_STATUS_SEL)

	owner = models.ForeignKey(User)
	template = models.ForeignKey('Image')

	def __unicode__(self):
		return self.name

class ServiceInstance(models.Model):
	name = models.CharField(max_length=80)
	status = models.CharField(max_length=1, choices=STATUS_SEL)
	point_used = models.IntegerField()
	point_plan = models.IntegerField()

	item = models.ForeignKey(ServiceItem)
	user = models.ForeignKey(User)

	cpus = models.IntegerField()
	memory = models.IntegerField()
	storage = models.IntegerField()

	def __unicode__(self):
		return self.name

class Image(models.Model):
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1, choices=IMAGE_TYPE_SEL)
	source = models.CharField(max_length=1, choices=SOURCE_SEL)
	is_template = models.BooleanField(default=False)
	is_pool = models.BooleanField(default=False)

	pool = models.CharField(max_length=128)
	volume = models.CharField(max_length=128)

	template = models.ForeignKey('self', null=True, blank=True)
	instance = models.ForeignKey(ServiceInstance, null=True, blank=True)

	def __unicode__(self):
		return self.name

