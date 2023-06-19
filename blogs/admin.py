from django.contrib import admin

from . models import Response, Posts

admin.site.register(Posts)
admin.site.register(Response)
