from django.db import models
from django.contrib.auth.models import User

from universe.models import Volume

# Create your models here.

TYPE_SEL = (
	('M', 'Virtual Machine'),
	('S', 'Storage'),
)

SOURCE_SEL = (
	('S', 'Standard'),
	('T', 'Third Party'),
	('B', 'Backup'),
	('C', 'Custom'),
)

RELEASE_STATUS_SEL = (
	('D', 'Draft'),
	('R', 'Released'),
	('P', 'Postponed'),
	('E', 'Expired'),
)

STATUS_SEL = (
	('N', 'New'),
	('A', 'Active'),
	('R', 'Running'),
	('S', 'Suspended'),
	('E', 'Expired'),
)


class ServiceItem(models.Model):
	name = models.CharField(max_length=80)
	type = models.CharField(max_length=1, choices=TYPE_SEL)
	description = models.CharField(max_length=256,null=True,blank=True)

	status = models.CharField(max_length=1,
			default='D', choices=RELEASE_STATUS_SEL)
	source = models.CharField(max_length=1,default='S',choices=SOURCE_SEL)

	owner = models.ForeignKey(User)

	template = models.ForeignKey(Volume,null=True,blank=True)
	num_spare = models.IntegerField(default=0)

	def __unicode__(self):
		return self.name

class ServiceInstance(models.Model):
	name = models.CharField(max_length=80)
	status = models.CharField(max_length=1,default='N',choices=STATUS_SEL)
	point_used = models.IntegerField()
	point_plan = models.IntegerField()

	item = models.ForeignKey(ServiceItem)
	user = models.ForeignKey(User)

	cpus = models.IntegerField()
	memory = models.IntegerField()
	storage = models.IntegerField()

	def __unicode__(self):
		return self.name

