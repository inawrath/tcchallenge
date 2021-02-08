import json

from django.db import models
from django.utils import timezone
from django_celery_beat.models import (
    IntervalSchedule,
    PeriodicTask,
)

from core.models import Asset


class Scraper(models.Model):
    """
    Model to store scrapers configuratioms
    """

    class Meta:
        verbose_name = 'Scraper'
        verbose_name_plural = 'Scrapers'

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    url = models.TextField(max_length=200)
    scrape_frecuency = models.IntegerField(default=5)
    active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    task = models.OneToOneField(
        PeriodicTask,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    def delete(self, *args, **kwargs):
        if self.task is not None:
            self.task.delete()

        return super(self.__class__, self).delete(*args, **kwargs)

    def setup_task(self):
        self.task = PeriodicTask.objects.create(
            name=self.asset.name,
            task='scrape_to_coindesk',
            interval=self.interval_schedule,
            args=json.dumps([self.id]),
            start_time=timezone.now()
        )
        self.save()

    @property
    def interval_schedule(self):
        print('interval_schedule')
        if len(IntervalSchedule.objects.filter(
            every=self.scrape_frecuency,
            period='minutes',
        )) == 0:
            interval_schedule = IntervalSchedule(
                every=self.scrape_frecuency,
                period='minutes',
            )
            interval_schedule.save()
        else:
            interval_schedule = IntervalSchedule.objects.get(
                every=self.scrape_frecuency,
                period='minutes',
            )
        return interval_schedule

    def __str__(self):
        return "%s - %s - %d minutes" % (self.asset, self.active, self.scrape_frecuency)
