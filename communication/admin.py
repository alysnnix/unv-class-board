from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_type', 'date', 'description', 'image')
    list_filter = ('message_type', 'date')