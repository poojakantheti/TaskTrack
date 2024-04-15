from django.db import models


class Label(models.Model):
    label_name = models.CharField(max_length=255)
    label_colour = models.CharField(max_length=100, choices=[
        ("#E91E63", "Deep Pink"),
        ("#9C27B0", "Purple"),
        ("#3F51B5", "Indigo"),
        ("#03A9F4", "Light Blue"),
        ("#00BCD4", "Cyan"),
        ("#4CAF50", "Green"),
        ("#CDDC39", "Lime"),
        ("#FFEB3B", "Yellow"),
        ("#FF9800", "Orange"),
        ("#795548", "Brown")])
    user = models.CharField(max_length=255, default='blank')


# Task db model
class Task(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.CharField(max_length=500)
    task_status = models.BooleanField()
    task_label = models.ForeignKey(Label, on_delete=models.CASCADE)
    user = models.CharField(max_length=255, default='blank')
    deadline = models.DateTimeField(null=True, blank=True)

