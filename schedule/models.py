from django.db import models
from core.models import Subject, Teacher, ClassGroup

class Schedule(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    ]
    day_of_week = models.CharField(max_length=20, choices=DAY_OF_WEEK_CHOICES, verbose_name="Day of the Week")
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    class Meta:
        db_table = 'schedule'
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"

    def __str__(self):
        return f"{self.class_group.name} - {self.subject.name} - {self.day_of_week}"