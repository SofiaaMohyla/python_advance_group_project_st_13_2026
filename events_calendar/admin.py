from django.contrib import admin
from .models import Event, EventImage

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'location')
    search_fields = ('title', 'description', 'location')
    list_filter = ('start_time', 'end_time', 'location')

class EventImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'image')
    search_fields = ('event__title',)

admin.site.register(Event, EventAdmin)
admin.site.register(EventImage, EventImageAdmin)