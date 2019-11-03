from django.contrib import admin

from .models import UrlHit, HitCount

admin.site.register(UrlHit)
admin.site.register(HitCount)

