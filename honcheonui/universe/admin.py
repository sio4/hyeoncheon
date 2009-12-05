from django.contrib import admin

from universe.models import *

admin.site.register(Constellation)
admin.site.register(Star)
admin.site.register(StarStatus)
admin.site.register(Light)
admin.site.register(LightStatus)
admin.site.register(Network)
admin.site.register(Pool)
admin.site.register(PoolStatus)
admin.site.register(Volume)
admin.site.register(VolumeStatus)

