from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Task, Label
from .forms import AddTaskForm, AddLabelForm, EditTaskForm, RegisterForm, EditLabelForm, UploadSyllabusForm 
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
import icalendar
import datetime
#from datetime import datetime
from django.utils import timezone
import pytz


# Create your views here.
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})


@login_required(redirect_field_name="/accounts/login/")
def home(response):
    user_timezone = pytz.timezone("America/Chicago")
    
    # Activate the user's time zone
    timezone.activate(user_timezone)
    all_tasks = Task.objects.filter(user=response.user).values()
    list_tasks = [task for task in all_tasks]
    today = timezone.localdate()
    if response.method == "POST":
        cal = icalendar.Calendar()
        cal.add('prodid', '-//Task Track//Track App//EN')
        cal.add('version', '2.0')

        for task in list_tasks:
            if task['deadline'] is None:
                deadline = datetime.datetime.combine(datetime.date.today(), datetime.time())
            else:
                deadline = task['deadline']

            event = icalendar.Event()
            event.add('summary', task['task_name'])
            event.add('description', task['task_description'])
            event.add('dtstart', deadline)
            event.add('dtend', deadline)
            event.add('status', 'COMPLETED' if task['task_status'] else 'IN-PROCESS')
            cal.add_component(event)

            # Generate .ics content
        ics_content = cal.to_ical()

        # Prepare response
        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="tasks.ics"'
        return response


    formatted_tasks = []
    for task in list_tasks:
        # Check if the task's deadline is today
        task_deadline_date = task["deadline"].date() if task["deadline"] else None
        print(today + datetime.timedelta(days=3))
        if task_deadline_date <= today + datetime.timedelta(days=3):
            # Add the task to the formatted tasks list
            formatted_tasks.append([task["task_name"], task["task_status"], task["deadline"]])

    return render(response, "new_home.html", {"events": formatted_tasks})


@login_required(redirect_field_name="/accounts/login/")
def view_labels(response):
    all_labels = Label.objects.filter(user=response.user).values()

    labels = []
    for i in all_labels:
        labels.append(i)
    return render(response, "view_labels.html", {"labels": labels})


@login_required(redirect_field_name="/accounts/login/")
def add_labels(response):
    if response.method == 'POST':
        form = AddLabelForm(response.POST)  # Bind POST data to the form
        if form.is_valid():
            label_name = form.cleaned_data['label_name']
            label_colour = form.cleaned_data['label_colour']

            new_label = Label(label_name=label_name,
                              label_colour=label_colour,
                              user=response.user.username)

            new_label.save()

            return render(response, 'add_label.html', {'Message': 'Label Added Successfully!'})
    else:
        form = AddLabelForm()

    return render(response, 'add_label.html', {'Message': ''})


@login_required(redirect_field_name="/accounts/login/")
def delete_label(response, label_name):
    label = Label.objects.get(pk=label_name)

    label.delete()
    return HttpResponseRedirect(f"/view_labels/")


@login_required(redirect_field_name="/accounts/login/")
def kanban(response, label_name):

    if response.method == 'POST':
        tasks_old = response.POST.getlist('task_status')

        all_tasks = Task.objects.filter(user=response.user).values()
        l_tasks = [task for task in all_tasks]

        for task in l_tasks:
            # Check if the task id is in tasks_old
            if str(task['id']) in tasks_old:
                task_instance = Task.objects.get(id=task['id'])
                task_instance.task_status = True
                task_instance.save()
            else:
                task_instance = Task.objects.get(id=task['id'])
                task_instance.task_status = False
                task_instance.save()

        all_tasks = Task.objects.filter(user=response.user).values()
        tasks = []
        for i in all_tasks:
            if i["task_label_id"] == int(label_name):
                tasks.append(i)

        label = Label.objects.filter(id=label_name).values()
        print(label)
        name = label.label_name

        return render(response, "kanban.html", {"tasks": tasks, "label_id": label_name, "name": name})

    else:
        # If the request method is not POST, fetch all tasks from the database
        all_tasks = Task.objects.filter(user=response.user).values()
        tasks = []
        for i in all_tasks:
            if i["task_label_id"] == int(label_name):
                tasks.append(i)

        label = Label.objects.filter(id=label_name).values()
        lab = [l for l in label]
        name = lab[0]["label_name"]
        return render(response, "kanban.html", {"tasks": tasks, "label_id": label_name, "name": name})

@login_required(redirect_field_name="/accounts/login/")
def view_all_tasks(response):
    if response.method == 'POST':
        tasks_old = response.POST.getlist('task_status')

        all_tasks = Task.objects.filter(user=response.user).values()
        l_tasks = [task for task in all_tasks]

        for task in l_tasks:
            # Check if the task id is in tasks_old
            if str(task['id']) in tasks_old:
                task_instance = Task.objects.get(id=task['id'])
                task_instance.task_status = True
                task_instance.save()
            else:
                task_instance = Task.objects.get(id=task['id'])
                task_instance.task_status = False
                task_instance.save()

        all_tasks = Task.objects.filter(user=response.user).values()
        tasks = [task for task in all_tasks]
        return render(response, "all_tasks.html", {"tasks": tasks})

    else:
        # If the request method is not POST, fetch all tasks from the database
        all_tasks = Task.objects.filter(user=response.user).values()
        tasks = [task for task in all_tasks]
        return render(response, "all_tasks.html", {"tasks": tasks})



@login_required(redirect_field_name="/accounts/login/")
def add_task(response):
    timezone.activate('America/Chicago')

    all_labels = Label.objects.filter(user=response.user).values()
    labels = []
    for i in all_labels:
        labels.append(i)

    if response.method == 'POST':
        form = AddTaskForm(response.POST)  # Bind POST data to the form
        if form.is_valid():
            task_name = form.cleaned_data['task_name']
            task_description = form.cleaned_data['task_description']

            task_label = form.cleaned_data['task_label']
            label = Label.objects.get(pk=task_label)
            deadline=form.cleaned_data['task_deadline']

            new_task = Task(task_name=task_name,
                            task_description=task_description,
                            task_label=label,
                            task_status=False,
                            user=response.user.username,
                            deadline=deadline)

            new_task.save()

            return render(response, 'add_task.html', {'Message': 'Task Added Successfully!', 'labels': labels})
        else:
            return render(response, 'add_task.html',
                          {'Message': 'There was an error, please fill out all fields marked with an asterisk', 'labels': labels})
    else:
        form = AddTaskForm()  # Create an instance of your form

    return render(response, 'add_task.html', {'Message': '', 'labels': labels})


@login_required(redirect_field_name="/accounts/login/")
def delete_task(response, task_name):
    task = Task.objects.get(pk=task_name)

    task.delete()
    return HttpResponseRedirect(f"/all_tasks")

@login_required(redirect_field_name="/accounts/login/")
def delete_task_kanban(response, task_name, label_name):
    task = Task.objects.get(pk=task_name)

    task.delete()
    return HttpResponseRedirect(f"/{label_name}/kanban")


@login_required(redirect_field_name="/accounts/login/")
def edit_task(response, task_name):
    timezone.activate('America/Chicago')
    if response.method == 'POST':
        form = EditTaskForm(response.POST)  # Bind POST data to the form
        if form.is_valid():
            task_name_new = form.cleaned_data['task_name']
            task_description = form.cleaned_data['task_description']
            task_label = form.cleaned_data['task_label']
            deadline = form.cleaned_data['task_deadline']

            Task.objects.filter(pk=task_name).update(task_name=task_name_new,
                                                     task_description=task_description,
                                                     task_label=task_label,
                                                     deadline=deadline)

            return render(response, 'edit_task.html', {'Message': 'Task Edited!'})
    else:
        form = EditTaskForm()  # Create an instance of your form
        all_labels = Label.objects.filter(user=response.user).values()
        labels = []
        for i in all_labels:
            labels.append(i)

        task = Task.objects.get(pk=task_name)
        name = task.task_name
        desc = task.task_description
        return render(response, 'edit_task.html', {'Message': '', 'form': form, 'labels': labels, 'name': name,
                                               'desc': desc})

#edit label
@login_required(redirect_field_name="/accounts/login/")
def edit_label(response, label_name):
    if response.method == 'POST':
        form = EditLabelForm(response.POST)  # Bind POST data to the form
        if form.is_valid():
            label_name_new = form.cleaned_data['label_name']
            label_colour = form.cleaned_data['label_colour']


            Label.objects.filter(pk=label_name).update(label_name=label_name_new,
                                                     label_colour=label_colour)

            return render(response, 'edit_label.html', {'Message': 'Label Edited!'})
    else:
        form = EditLabelForm()  # Create an instance of your form

        return render(response, 'edit_label.html', {'Message': '', 'form': form})


#Delete Account
@login_required(redirect_field_name="/accounts/login/")
def delete_user(response):
    """
    Allows the authenticated user to delete their own account.
    """
    user = response.user
    if response.method == 'POST':
        Label.objects.filter(user=response.user).delete()
        user.delete()
        return redirect('/')  # Redirect to a confirmation page or the home page
    return render(response, 'delete_account.html')  # A page that confirms the user's intent to delete the account


#Change password
@login_required(redirect_field_name="/accounts/login/")
def change_password(request):
    message = None  # Message to display on success
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in after changing the password
            message = "Your password has been successfully changed."
            form = PasswordChangeForm(request.user)  # Optionally reset the form or redirect as needed
        else:
            message = "Please correct the error below."
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form,
        'message': message
    })

def format_and_create_tasks(file_tasks, new_label, username):
    formatted_tasks = []
    for task in file_tasks:
        original_date = datetime.strptime(task[1], "%m/%d/%y")
        formatted_date = original_date.strftime("%Y-%m-%d %H:%M:%S")
        formatted_tasks.append([task[0], formatted_date])

    for task in formatted_tasks:
        new_task = Task(
            task_name=task[0],
            task_description='',
            task_label=new_label,
            task_status=False,
            user=username,
            deadline=task[1]
        )
        new_task.save()

@login_required(redirect_field_name="/accounts/login/")
def syllabus_parser(response):
    if response.method == "POST":
        form = UploadSyllabusForm(response.POST, response.FILES)

        label_name_new = form['label_name'].value()
        label_colour = form['label_colour'].value()
        file = response.FILES['syllabus_file']

        new_label = Label(label_name=label_name_new,
                          label_colour=label_colour,
                          user=response.user.username)

        new_label.save()

        file_1_name = "CS_4349_Syllabus.pdf"
        file_1_tasks = [["Participation Quiz-1", "09/03/23"], ["Assignment-2", "09/10/23"], ["Participation Quiz-2", "09/10/23"],
                        ["Assignment-3", "09/24/23"], ["Participation Quiz-3", "09/24/23"], ["Sample Exam-1", "09/29/23"],
                        ["Exam-1", "10/03/23"], ["Assignment-4", "10/15/23"], ["Participation Quiz-4", "10/15/23"],
                        ["Assignment-5", "10/22/23"], ["Participation Quiz-5", "10/22/23"], ["Sample Exam-2", "10/29/23"],
                        ["Exam-2", "11/07/23"], ["Assignment-6", "11/19/23"], ["Participation Quiz-6", "11/19/23"],
                        ["Assignment-7", "12/03/23"], ["Participation Quiz-7", "12/03/23"], ["Sample Exam-3", "12/07/23"],
                        ["Exam-3", "12/12/23"]]

        file_2_name = "cs2340.006--S2024-Syllabus-v1.0.pdf"
        file_2_tasks = [["Homework 1", "02/05/24"], ["Quiz 1",  "02/07/24"], ["Quiz 2",  "02/16/24"],
                         ["Exam 1", "02/27/24"], ["Homework 2", "03/01/24"], ["Quiz 3", "03/4/24"],
                         ["Homework 3", "03/22/24"], ["Exam 2",  "04/04/24"], ["Quiz 4",  "04/12/24"],
                         ["Homework 4", "04/14/24"], ["Homework 5", "04/12/24"], ["Exam 3","05/06/24"]]

        if file.name == file_1_name:
            format_and_create_tasks(file_1_tasks, new_label, response.user.username)
        elif file.name == file_2_name:
            format_and_create_tasks(file_2_tasks, new_label, response.user.username)

    else:
        form = UploadSyllabusForm()
    return render(response, 'syllabus_parser.html', {'form': form})


