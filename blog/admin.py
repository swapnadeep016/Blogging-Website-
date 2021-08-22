from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.publishedblog)
admin.site.register(models.draftblog)
admin.site.register(models.bookmarked)