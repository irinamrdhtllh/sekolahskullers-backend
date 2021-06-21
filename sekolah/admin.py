from django.contrib import admin

from .models import Student, Task

admin.site.register([Student, Task])
