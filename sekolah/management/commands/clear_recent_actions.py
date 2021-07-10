from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry


class Command(BaseCommand):
    help = 'Clear recent actions in admin site'

    def handle(self, *args, **options):
        count = LogEntry.objects.count()
        plural = count == 1 if True else False

        LogEntry.objects.all().delete()

        self.stdout.write(
            f'Successfully cleared {count} recent action' + ('s' if plural else '')
        )
