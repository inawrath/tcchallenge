from django.test import TestCase, TransactionTestCase
from model_bakery import baker

from core.models import (
    Asset,
    AssetData,
    Scraper,
)
from core.scrapers import CoindeskScraper
from core.tasks import scrape_to_coindesk


class AssetTest(TestCase):
    def setUp(self):
        super(AssetTest, self).setUp()

        self.data = baker.make(
           Asset,
           name='Dodge Coin',
           description='Dodge Coin Asset'
        )

    def test_procesar_archivo(self):
        qs = Asset.objects.all()
        self.assertEquals(qs.count(), 1)

    def test_get_str_asset(self):
        qs = Asset.objects.all()
        self.assertEqual(str(qs[0]), str(self.data))


class AssetDataTest(TestCase):
    def setUp(self):
        super(AssetDataTest, self).setUp()
        self.data = baker.make(AssetData, _quantity=5)

    def test_data(self):
        for x in self.data:
            print(x.low_24h, x.high_24h, x.price)
        self.assertEquals(len(self.data), 5)

    def test_str(self):
        qs = AssetData.objects.all()
        for data, data_query in zip(self.data, qs):
            self.assertEqual(str(data), str(data_query))


class ScraperTest(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        super(ScraperTest, self).setUp()
        self.data = baker.make(Scraper, _quantity=2)

    def test_data(self):
        self.assertEqual(len(self.data), 2)


class CoindeskTest(TestCase):
    def setUp(self):
        super(CoindeskTest, self).setUp()

    def test_valid_url_coindesk(self):
        scraper = CoindeskScraper(url='https://www.coindesk.com/price/bitcoin')
        self.failIfEqual(scraper.get_detail(), {})

    def test_invalid_url_coindesk(self):
        with self.assertRaises(Exception):
            CoindeskScraper(url='https://www.coindesk.com/price/invalid')

    def test_invalid_host(self):
        with self.assertRaises(Exception):
            CoindeskScraper(url='https://www.coin-desk.com/price/bitcoin')


class ScraperTaskCeleryTest(TestCase):
    def setUp(self):
        super(ScraperTaskCeleryTest, self).setUp()
        self.data = baker.make(
            Scraper,
            url='https://www.coindesk.com/price/bitcoin',
        )

    def test_call_scraper(self):
        result = scrape_to_coindesk(self.data.id)
        self.assertIsNone(result)
