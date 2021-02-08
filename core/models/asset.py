from django.db import models


class Asset(models.Model):
    """
    Model to store the assets
    """
    name = models.CharField(max_length=100, unique=True) # Bitcoin, Etherium scraper
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.description)
