from django.contrib import admin
from django.contrib.auth.models import Group as AdminGroup

from . import models

admin.site.unregister(AdminGroup)


### Student ###


class AssessmentInline(admin.StackedInline):
    model = models.Assessment


class StudentInline(admin.TabularInline):
    model = models.Student


class StudentTaskStatusInline(admin.TabularInline):
    model = models.StudentTask.students.through


class StudentAdmin(admin.ModelAdmin):
    inlines = (
        AssessmentInline,
        StudentTaskStatusInline,
    )
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


class StudentTaskAdmin(admin.ModelAdmin):
    inlines = (StudentTaskStatusInline,)
    exclude = ('students',)
    ordering = ('deadline', 'is_required')
    list_display = ('name', 'required_status', 'deadline', 'max_score')

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required


class StudentTaskStatusAdmin(admin.ModelAdmin):
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


admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.StudentTask, StudentTaskAdmin)
admin.site.register(models.StudentTaskStatus, StudentTaskStatusAdmin)


### Group ###


class GroupTaskStatusInline(admin.TabularInline):
    model = models.GroupTask.groups.through


class GroupAdmin(admin.ModelAdmin):
    inlines = (
        GroupTaskStatusInline,
        StudentInline,
    )
    list_display = ('name', 'health', 'exp', 'level')


class GroupTaskAdmin(admin.ModelAdmin):
    inlines = (GroupTaskStatusInline,)
    exclude = ('groups',)
    ordering = ('deadline', 'is_required')
    list_display = ('name', 'required_status', 'deadline', 'max_score')

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required


class GroupTaskStatusAdmin(admin.ModelAdmin):
    ordering = ('is_complete', 'group__name')
    list_display = ('group_name', 'task_name', 'complete_status', 'score')

    @admin.display(ordering='group__name', description='Name')
    def group_name(self, taskstatus):
        return taskstatus.group.name

    @admin.display(ordering='task__name', description='Task')
    def task_name(self, taskstatus):
        return taskstatus.task.name

    @admin.display(boolean=True, ordering='is_complete', description='Complete Status')
    def complete_status(self, taskstatus):
        return taskstatus.is_complete


admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.GroupTask, GroupTaskAdmin)
admin.site.register(models.GroupTaskStatus, GroupTaskStatusAdmin)


### Class Year ###


class MissionInline(admin.StackedInline):
    model = models.Mission


class ClassYearAdmin(admin.ModelAdmin):
    inlines = (MissionInline,)
    list_display = ('name', 'health', 'exp', 'level')


class ClassYearTaskAdmin(admin.ModelAdmin):
    ordering = ('deadline', 'is_required')
    list_display = (
        'name',
        'required_status',
        'deadline',
        'max_score',
        'complete_status',
        'score',
    )
    fieldsets = (
        (
            None,
            {
                "fields": ('name', 'is_required', 'deadline', 'max_score'),
            },
        ),
        (
            'Task status',
            {
                "fields": ('class_year', 'is_complete', 'score'),
            },
        ),
    )

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required

    @admin.display(boolean=True, ordering='is_complete', description='Complete Status')
    def complete_status(self, task):
        return task.is_complete


admin.site.register(models.ClassYear, ClassYearAdmin)
admin.site.register(models.ClassYearTask, ClassYearTaskAdmin)
