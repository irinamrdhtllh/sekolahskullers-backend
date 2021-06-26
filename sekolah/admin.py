from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .models import Student, Task, TaskStatus


class StudentAdmin(admin.ModelAdmin):
    ordering = ('user__username',)
    list_display = ('username', 'full_name', 'health', 'exp', 'level')

    @admin.display(ordering='user__username')
    def username(self, student):
        return student.user.get_username()

    @admin.display(ordering='user__first_name')
    def full_name(self, student):
        return student.user.get_full_name()

    @admin.display(description='Level', ordering='student__level')
    def level(self, student):
        return student.get_level_display()


class TaskAdmin(admin.ModelAdmin):
    ordering = ('deadline', 'is_required')
    list_display = ('name', 'required_status', 'deadline', 'max_score')

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required


class TaskStatusAdmin(admin.ModelAdmin):
    ordering = ('is_complete', 'student__user__username')
    list_display = ('username', 'full_name', 'task_name', 'complete_status', 'score')

    @admin.display(ordering='student__user__username')
    def username(self, taskstatus):
        return taskstatus.student.user.get_username()

    @admin.display(ordering='student__user__first_name')
    def full_name(self, taskstatus):
        return taskstatus.student.user.get_full_name()

    @admin.display(ordering='task__name', description='Task')
    def task_name(self, taskstatus):
        return taskstatus.task.name

    @admin.display(boolean=True, ordering='is_complete', description='Complete Status')
    def complete_status(self, taskstatus):
        return taskstatus.is_complete


TokenAdmin.raw_id_fields = ['user']

admin.site.register(Student, StudentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(TaskStatus, TaskStatusAdmin)
