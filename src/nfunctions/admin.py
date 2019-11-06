from django.contrib import admin

from .models import UrlHit, HitCount, Notification

admin.site.register(UrlHit)
admin.site.register(HitCount)
admin.site.register(Notification)

