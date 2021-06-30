from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assessment, Student


@receiver(post_save, sender=Student)
def create_on_register(sender, instance, created, **kwargs):
    if created:
        Assessment.objects.create(student=instance)
