from django.db import models

class Message(models.Model):
    MESSAGE_TYPES = [
        ("communication", "Communication"),
        ("event", "Event"),
        ("observation", "Observation"),
        ("pedagogical", "Pedagogical"),
    ]

    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, verbose_name="Type")
    date = models.DateField()
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to="images/user", blank=True, null=True)

    class_groups = models.ManyToManyField('core.ClassGroup', blank=True, related_name='messages')
    teachers = models.ManyToManyField('core.Teacher', blank=True, related_name='messages')

    class Meta:
        db_table = 'message'
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return self.get_message_type_display()