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


class ServiceItem(models.Model):
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1, choices=TYPE_SEL)

	owner = models.ForeignKey(User)
	template = models.ForeignKey('ImageTemplate')

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

class ImageTemplate(models.Model):
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1, choices=IMAGE_TYPE_SEL)
	pool = models.CharField(max_length=128)
	volume = models.CharField(max_length=128)
	source = models.CharField(max_length=1, choices=SOURCE_SEL)

	def __unicode__(self):
		return self.name

class Image(models.Model):
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1, choices=IMAGE_TYPE_SEL)
	pool = models.CharField(max_length=128)
	volume = models.CharField(max_length=128)

	template = models.ForeignKey(ImageTemplate)
	instance = models.ForeignKey(ServiceInstance)

	def __unicode__(self):
		return self.name

