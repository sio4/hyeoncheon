from django.contrib import admin

from universe.models import *

class StarInline(admin.TabularInline):
	fieldsets = [
		(None,{'fields':['name','uri','constellation']}),
	]
	model = Star
	extra = 1

class PoolInline(admin.TabularInline):
	fieldsets = [
		(None, {'fields':['name','uuid','type','capacity']}),
	]
	model = Pool
	extra = 1

class PoolStatusInline(admin.TabularInline):
	model = PoolStatus
	extra = 1

class PoolLinkInline(admin.TabularInline):
	model = PoolLink
	extra = 1

class VolumeInline(admin.TabularInline):
	fieldsets = [
		(None, {'fields':['name','uuid','type','capacity']}),
	]
	model = Volume
	extra = 1

class VolumeStatusInline(admin.TabularInline):
	fieldsets = [
		(None, {'fields':['allocation']}),
	]
	model = VolumeStatus
	extra=0

class LightInline(admin.TabularInline):
	fieldsets = [
		(None, {'fields':['name','uuid','constellation']}),
	]
	model = Light
	extra = 1

class LightStatusInline(admin.TabularInline):
	fieldsets = [
		(None, {'fields':['state','star','cputime']}),
	]
	model = LightStatus
	extra = 0

class StarAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['name','uri','constellation']}),
		('Spec', {'fields':['memory','cpus','mhz']}),
		('More', {'fields':['hostname','type','model','version'],
			'classes':['collapse']}),
	]
	list_display = ('name','uri','constellation')

class LightAdmin(admin.ModelAdmin):
	list_display = ('name','uuid','constellation','type','cpus','memory')
	inlines = [LightStatusInline]

class ConstellationAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['name']}),
		('More', {'fields':['location','description','version'],
			'classes':['collapse']}),
	]
	list_display = ('name','location','description')
	inlines = [StarInline, LightInline, PoolInline]

class PoolAdmin(admin.ModelAdmin):
	fieldsets = [
		(None, {'fields':['name','uuid','constellation','capacity']}),
		('More', {'fields':['type','path','is_shared',
			'hostname','export','version'],
			'classes':['collapse']}),
	]
	list_display = ('name','constellation','uuid','capacity')
	inlines = [PoolStatusInline, PoolLinkInline, VolumeInline]

class VolumeAdmin(admin.ModelAdmin):
	list_display = ('name','pool','capacity')
	inlines = [VolumeStatusInline]

admin.site.register(Constellation, ConstellationAdmin)
admin.site.register(Star,StarAdmin)
admin.site.register(StarStatus)
admin.site.register(Light,LightAdmin)
admin.site.register(LightStatus)
admin.site.register(Network)
admin.site.register(Pool, PoolAdmin)
admin.site.register(PoolStatus)
admin.site.register(PoolLink)
admin.site.register(Volume,VolumeAdmin)
admin.site.register(VolumeStatus)

