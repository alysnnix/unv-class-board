from django.contrib import admin
from .models import TeacherAbsence, TeacherSubstitution

@admin.register(TeacherAbsence)
class TeacherAbsenceAdmin(admin.ModelAdmin):
    list_display = ('get_formatted_start_date', 'get_formatted_end_date', 'teacher', 'justification')
    list_filter = ('start_date', 'teacher')

    def get_formatted_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d')
    get_formatted_start_date.short_description = 'Start Date'

    def get_formatted_end_date(self, obj):
        return obj.end_date.strftime('%Y-%m-%d')
    get_formatted_end_date.short_description = 'End Date'


@admin.register(TeacherSubstitution)
class TeacherSubstitutionAdmin(admin.ModelAdmin):
    list_display = ('get_formatted_start_date', 'get_formatted_end_date', 'absent_teacher', 'substitute_teacher')
    list_filter = ('start_date', 'substitute_teacher')

    def get_formatted_start_date(self, obj):
        return obj.start_date.strftime('%Y-%m-%d')
    get_formatted_start_date.short_description = 'Start Date'

    def get_formatted_end_date(self, obj):
        return obj.end_date.strftime('%Y-%m-%d')
    get_formatted_end_date.short_description = 'End Date'