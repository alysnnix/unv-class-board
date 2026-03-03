from django.db import models
from django.core.exceptions import ValidationError
from core.models import Subject, Teacher, ClassGroup

class Schedule(models.Model):
    DAY_OF_WEEK_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
    ]
    day_of_week = models.CharField(max_length=20, choices=DAY_OF_WEEK_CHOICES, verbose_name="Day of the Week", db_index=True)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.CASCADE, related_name='schedules')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    class Meta:
        db_table = 'schedule'
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        constraints = [
            # A teacher cannot be in two different classes at the exact same time
            models.UniqueConstraint(
                fields=['teacher', 'day_of_week', 'start_time'],
                name='unique_teacher_schedule_time'
            ),
            # A class group cannot have two different subjects at the exact same time
            models.UniqueConstraint(
                fields=['class_group', 'day_of_week', 'start_time'],
                name='unique_classgroup_schedule_time'
            )
        ]

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time.")
            
        if self.teacher and self.subject:
            if not self.teacher.subjects.filter(id=self.subject.id).exists():
                raise ValidationError(f"The teacher {self.teacher.name} is not qualified to teach {self.subject.name}.")

    def __str__(self):
        return f"{self.class_group.name} - {self.subject.name} - {self.day_of_week}"