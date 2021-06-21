from django.contrib import admin

from .models import Student, Task, StudentTaskStatus


class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'health', 'exp', 'level')

    @admin.display(description='Name', ordering='user__first_name')
    def full_name(self, student):
        return student.user.get_full_name()


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_required', 'deadline', 'max_score')


class StudentTaskStatusAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'task_name', 'is_finished', 'score')

    @admin.display(description='Name', ordering='student__user__first_name')
    def full_name(self, status):
        return status.student.user.get_full_name()

    @admin.display(description='Task', ordering='task__name')
    def task_name(self, status):
        return status.task.name


admin.site.register(Student, StudentAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(StudentTaskStatus, StudentTaskStatusAdmin)
