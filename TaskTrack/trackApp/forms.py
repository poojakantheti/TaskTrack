from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AddTaskForm(forms.Form):
    task_name = forms.CharField(label='task name', max_length=255, required=True)
    task_description = forms.CharField(label='task description', max_length=500, required=False)
    task_label = forms.CharField(label='task label', max_length=100, required=True)
    task_deadline = forms.DateTimeField(label='task deadline', required=True)


class SaveTaskForm(forms.Form):
    task_name = forms.CharField(label='task name', max_length=255, required=True)
    task_description = forms.CharField(label='task description', max_length=500, required=False)
    task_label = forms.CharField(label='task label', max_length=100, required=False)
    task_status = forms.BooleanField(label="task status")


class AddLabelForm(forms.Form):
    label_name = forms.CharField(label='label name', max_length=255, required=True)
    label_colour = forms.ChoiceField(label="label colour", choices=[
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


class EditTaskForm(forms.Form):
    task_name = forms.CharField(label='task name', max_length=255, required=True)
    task_description = forms.CharField(label='task description', max_length=500, required=False)
    task_label = forms.CharField(label='task label', max_length=100, required=False)
    task_deadline = forms.DateTimeField(label='task deadline', required=True)

class EditLabelForm(forms.Form):
    label_name = forms.CharField(label='label name', max_length=255, required=True)
    label_colour = forms.ChoiceField(label="label colour", choices=[
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

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class UploadSyllabusForm(forms.Form):
    label_name = forms.CharField(label='label name', max_length=255, required=True)
    label_colour = forms.ChoiceField(label="label colour", choices=[
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
    syllabus_file = forms.FileField()
