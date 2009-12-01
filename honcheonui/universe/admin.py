from django.contrib import admin

from universe.models import *

admin.site.register(Constellation)
admin.site.register(Star)
admin.site.register(StarStatus)
admin.site.register(Light)
admin.site.register(LightStatus)
admin.site.register(Network)
admin.site.register(StoragePool)
admin.site.register(StoragePoolStatus)
admin.site.register(StorageVolume)
admin.site.register(StorageVolumeStatus)

