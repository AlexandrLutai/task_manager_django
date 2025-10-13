from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Task, TaskList

admin.site.register(Task)
admin.site.register(TaskList)