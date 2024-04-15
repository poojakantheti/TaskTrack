"""
URL configuration for TaskTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("<str:label_name>/kanban/", views.kanban, name="kanban"),
    path("all_tasks/", views.view_all_tasks, name="view all tasks"),
    path("add_task/", views.add_task, name="add task"),
    path("view_labels/", views.view_labels, name="view label"),
    path("add_label/", views.add_labels, name="add label"),
    path("delete_label/<str:label_name>/", views.delete_label, name="delete label"),
    path("delete_task/<str:task_name>/", views.delete_task, name="delete task"),
    path("delete_task_kanban/<str:label_name>/<str:task_name>/", views.delete_task_kanban, name="delete task"),
    path("edit_task/<str:task_name>/", views.edit_task, name="edit task"),
    path("edit_label/<str:label_name>/", views.edit_label, name="edit label"),
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("delete_account/", views.delete_user, name='delete_account'),
    path('change_password/', views.change_password, name='change_password'),
    path('upload_syllabus/', views.syllabus_parser, name='upload syllabus'), 
]
