from rest_framework import generics

from core.models import Scraper
from core.serializers import ScraperSerializer


class ScraperList(generics.ListCreateAPIView):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer


class ScraperDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer
