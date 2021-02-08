from rest_framework import serializers

from core.models import Scraper


class ScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scraper
        exclude = ('task', )
