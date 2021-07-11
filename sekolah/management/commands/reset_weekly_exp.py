from django.core.management.base import BaseCommand

from sekolah.models import Student, Group


class Command(BaseCommand):
    help = 'Reset weekly experience on Student and Group'

    def handle(self, *args, **options):
        students = Student.objects.all()
        num_student = 0
        for student in students:
            if student.weekly_exp == 0:
                continue

            student.weekly_exp = 0
            student.save()

            num_student += 1

        groups = Group.objects.all()
        num_group = 0
        for group in groups:
            if group.weekly_exp == 0:
                continue

            group.weekly_exp = 0
            group.save()

            num_group += 1

        self.stdout.write(
            f'Successfully cleared weekly experience on:\n\t{num_student} student'
            + ('' if num_student <= 1 else 's')
            + f'\n\t{num_group} group'
            + ('' if num_group <= 1 else 's')
        )
