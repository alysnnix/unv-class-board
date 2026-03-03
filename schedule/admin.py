from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'class_group', 'subject', 'teacher', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'class_group', 'subject', 'teacher')