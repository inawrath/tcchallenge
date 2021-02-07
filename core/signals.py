from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from core.models import Scraper


@receiver(post_save, sender=Scraper)
def create_or_update_periodic_task(sender, instance: Scraper, created, **kwargs):
    if created:
        instance.setup_task()
    else:
        if instance.task is not None:
            if instance.task.schedule.seconds != instance.scrape_frecuency * 60:
                task = instance.task
                instance.task = None
                instance.save()
                task.delete()
                instance.setup_task()
            else:
                instance.task.enabled = instance.active is True
                instance.task.save()

@receiver(post_delete, sender=Scraper)
def delete_task(sender, instance, **kwargs):
    if instance.task is not None:
        instance.task.delete()
