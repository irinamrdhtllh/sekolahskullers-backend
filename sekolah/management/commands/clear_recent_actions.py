from django.core.management.base import BaseCommand
from django.contrib.admin.models import LogEntry


class Command(BaseCommand):
    help = 'Clear recent actions in admin site'

    def handle(self, *args, **options):
        count = LogEntry.objects.count()

        LogEntry.objects.all().delete()

        self.stdout.write(
            f'Successfully cleared {count} recent action' + ('' if count <= 1 else 's')
        )
