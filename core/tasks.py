from celery import shared_task
from django.db import transaction
from django.utils import timezone
from time import sleep
from random import randint

from core.models import (
    AssetData,
    Scraper,
)
from core.scrapers import CoindeskScraper

@shared_task(name="scrape_to_coindesk")
def scrape_to_coindesk(scraper_id) -> None:
    try:
        scraper: Scraper = Scraper.objects.get(id=scraper_id)
        coindesk: CoindeskScraper = CoindeskScraper(url=scraper.url)

        data_scraper: dict = coindesk.get_detail()

        asset_data: AssetData = AssetData(**data_scraper)
        asset_data.asset = scraper.asset
        asset_data.data_datetime = timezone.now()

        asset_data.save()

        print(f'Add data to {scraper.asset.name}')
        del coindesk
        del data_scraper
        del asset_data

    except Exception as e:
        print(e)
        print(f'Problem with scrape {scraper_id}')
