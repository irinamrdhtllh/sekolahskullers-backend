from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Student, Task, StudentTaskStatus


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)

    list_display = ('username', 'full_name', 'health', 'exp', 'level')

    @admin.display(description='Name', ordering='first_name')
    def full_name(self, user):
        return user.get_full_name()

    @admin.display(description='Health', ordering='student__health')
    def health(self, user):
        return user.student.health

    @admin.display(description='Experience', ordering='student__exp')
    def exp(self, user):
        return user.student.exp

    @admin.display(description='Level')
    def level(self, user):
        return user.student.level


class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_required', 'deadline', 'max_score')


class StudentTaskStatusAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'task_name', 'is_complete', 'score')

    @admin.display(description='Name', ordering='student__user__first_name')
    def full_name(self, status):
        return status.student.user.get_full_name()

    @admin.display(description='Task', ordering='task__name')
    def task_name(self, status):
        return status.task.name


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(StudentTaskStatus, StudentTaskStatusAdmin)
