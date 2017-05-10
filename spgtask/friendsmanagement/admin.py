# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Relationship

# Register your models here.
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'status')

admin.site.register(Relationship, RelationshipAdmin)
