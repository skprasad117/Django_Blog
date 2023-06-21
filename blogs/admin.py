from django.contrib import admin

from . models import Response, Posts, CommentsResponse, BlogGallery, Subscription

admin.site.register(Posts)
admin.site.register(Response)
admin.site.register(CommentsResponse)
admin.site.register(BlogGallery)
admin.site.register(Subscription)
