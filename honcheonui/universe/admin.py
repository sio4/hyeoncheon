from django.contrib import admin

from universe.models import *

admin.site.register(Constellation)
admin.site.register(Star)
admin.site.register(Network)
admin.site.register(StoragePool)

