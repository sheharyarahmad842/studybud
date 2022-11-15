from django.contrib import admin
from .models import Topic, Room, Message

# Register your models here.
class RoomInline(admin.StackedInline):
    model = Room


class TopicAdmin(admin.ModelAdmin):
    inlines = [
        RoomInline,
    ]

class MessageInline(admin.StackedInline):
    model = Message

class RoomAdmin(admin.ModelAdmin):
    inlines = [
        MessageInline,
    ]
    list_display = ("name", "updated_on", "created_on")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


admin.site.register(Topic, TopicAdmin)
admin.site.register(Room, RoomAdmin)
