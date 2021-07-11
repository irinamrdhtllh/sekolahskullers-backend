from django.contrib import admin
from django.contrib.auth.models import Group as AdminGroup

from . import models

admin.site.unregister(AdminGroup)


### Student ###


class AssessmentInline(admin.StackedInline):
    model = models.Assessment
    extra = 1


class StudentInline(admin.TabularInline):
    model = models.Student
    extra = 1
    raw_id_fields = ('user',)

    def has_add_permission(self, request, obj):
        return False


class StudentTaskStatusInline(admin.TabularInline):
    model = models.StudentTask.students.through
    extra = 1
    raw_id_fields = ('task',)

    def has_add_permission(self, request, obj):
        return False


class StudentAdmin(admin.ModelAdmin):
    inlines = (
        AssessmentInline,
        StudentTaskStatusInline,
    )
    list_display = ('username', 'full_name', 'health', 'exp', 'level')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    save_on_top = True

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
    save_on_top = True

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required


admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.StudentTask, StudentTaskAdmin)


### Group ###


class GroupTaskStatusInline(admin.TabularInline):
    model = models.GroupTask.groups.through
    extra = 1
    raw_id_fields = ('group', 'task')

    def has_add_permission(self, request, obj):
        return False


class GroupAdmin(admin.ModelAdmin):
    inlines = (
        StudentInline,
        GroupTaskStatusInline,
    )
    list_display = ('name', 'health', 'exp', 'level')
    save_on_top = True


class GroupTaskAdmin(admin.ModelAdmin):
    inlines = (GroupTaskStatusInline,)
    exclude = ('groups',)
    ordering = ('deadline', 'is_required')
    list_display = ('name', 'required_status', 'deadline', 'max_score')
    save_on_top = True

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required


admin.site.register(models.Group, GroupAdmin)
admin.site.register(models.GroupTask, GroupTaskAdmin)


### Class Year ###


class MissionInline(admin.StackedInline):
    model = models.Mission
    extra = 1


class ClassYearAdmin(admin.ModelAdmin):
    inlines = (MissionInline,)
    list_display = ('name', 'health', 'exp', 'level')
    save_on_top = True


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
                'fields': ('name', 'is_required', 'deadline', 'max_score'),
            },
        ),
        (
            'STATUS TUGAS ANGKATAN',
            {
                'fields': ('class_year', 'is_complete', 'score'),
            },
        ),
    )
    save_on_top = True

    @admin.display(boolean=True, ordering='is_required', description='Required Status')
    def required_status(self, task):
        return task.is_required

    @admin.display(boolean=True, ordering='is_complete', description='Complete Status')
    def complete_status(self, task):
        return task.is_complete


admin.site.register(models.ClassYear, ClassYearAdmin)
admin.site.register(models.ClassYearTask, ClassYearTaskAdmin)
