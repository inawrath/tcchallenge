from django.db import models

from core.models import Asset


class AssetData(models.Model):
    """
    Model to store the assets information
    """
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.FloatField()
    low_24h = models.FloatField()
    high_24h = models.FloatField()
    returns_24h = models.FloatField()
    returns_ytd = models.FloatField()
    volatility = models.FloatField()
    data_datetime = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.asset.name} - {self.price} - {self.data_datetime}'
