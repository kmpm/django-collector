# coding=utf-8
from models import *
from django.contrib import admin




class TagLogInline(admin.TabularInline):
    model = TagLog
    extra=0

class TagAdmin(admin.ModelAdmin):
    list_display=['name', 'enabled', 'driver', 'device', 'address', 'cv', 'pv', 'sv', 'last_read_at', 'last_change_at', 'comment']
    inlines= [TagLogInline]
    list_filter = ['driver', 'device']
    search_fields = ['name']
admin.site.register(Tag, TagAdmin)




class TagLogAdmin(admin.ModelAdmin):
    list_display=['id', 'tag', 'v', 'created_at']
    list_filter = ['tag']

admin.site.register(TagLog, TagLogAdmin)

admin.site.register(Driver)