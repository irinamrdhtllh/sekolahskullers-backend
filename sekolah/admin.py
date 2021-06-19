from django.contrib import admin

from .models import Year, Group, Student, TaskYear, TaskGroup, TaskStudent

admin.site.register([Year, Group, Student, TaskYear, TaskGroup, TaskStudent])
