from django.db import models
from django.core.exceptions import ValidationError
from core.models import Teacher, Justification

class TeacherAbsence(models.Model):
    start_date = models.DateField(verbose_name="Start Date", db_index=True)
    end_date = models.DateField(verbose_name="End Date", db_index=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='absences')
    justification = models.ForeignKey(Justification, on_delete=models.CASCADE, related_name='absences')

    class Meta:
        db_table = 'teacher_absence'
        verbose_name = "Teacher Absence"
        verbose_name_plural = "Teacher Absences"
        
    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")

    def __str__(self):
        return f"{self.teacher.name} - {self.start_date.strftime('%d/%m/%Y')}"

class TeacherSubstitution(models.Model):
    start_date = models.DateField(verbose_name="Start Date", db_index=True)
    end_date = models.DateField(verbose_name="End Date", db_index=True)
    absent_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="substitutions_needed")
    substitute_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="substitutions_provided")

    class Meta:
        db_table = 'teacher_substitution'
        verbose_name = "Teacher Substitution"
        verbose_name_plural = "Teacher Substitutions"

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date cannot be after end date.")
        if self.absent_teacher == self.substitute_teacher:
            raise ValidationError("A teacher cannot substitute themselves.")

    def __str__(self):
        return f"{self.substitute_teacher.name} for {self.absent_teacher.name} on {self.start_date.strftime('%d/%m/%Y')}"