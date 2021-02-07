from celery import shared_task
from django.utils import timezone

from core.models import (
    AssetData,
    Scraper,
)
from core.scrapers.coindesk import CoindeskScraper

@shared_task(name="scrape_to_coindesk")
def scrape_to_coindesk(scraper_id) -> None:

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
