from django.db import models
from django.core.validators import RegexValidator

class Subject(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'subject'
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.name

class Teacher(models.Model):
    name = models.CharField(max_length=200)
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, verbose_name="Phone Number")
    
    # Applied SOLID/Normalization: Instead of a text field for subjects, use a ManyToMany relationship
    subjects = models.ManyToManyField(Subject, related_name="teachers", verbose_name="Subjects")
    is_substitute = models.BooleanField(default=False, verbose_name="Is Substitute")

    class Meta:
        db_table = 'teacher'
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return self.name

class Justification(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'justification'
        verbose_name = "Justification"
        verbose_name_plural = "Justifications"

    def __str__(self):
        return self.name

class SchoolSegment(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'school_segment'
        verbose_name = "School Segment"
        verbose_name_plural = "School Segments"

    def __str__(self):
        return self.name

class SchoolPeriod(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'school_period'
        verbose_name = "School Period"
        verbose_name_plural = "School Periods"

    def __str__(self):
        return self.name

class ClassGroup(models.Model):
    name = models.CharField(max_length=200)
    segment = models.ForeignKey(SchoolSegment, on_delete=models.CASCADE, related_name='classes')
    period = models.ForeignKey(SchoolPeriod, on_delete=models.CASCADE, related_name='classes')

    class Meta:
        db_table = 'class_group'
        verbose_name = "Class Group"
        verbose_name_plural = "Class Groups"

    def __str__(self):
        return self.name