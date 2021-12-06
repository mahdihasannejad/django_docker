from django.db import models


class Games(models.Model):
    Rank = models.SmallIntegerField(default=0)
    Name = models.CharField(max_length=200)
    Platform = models.CharField(max_length=10)
    Year = models.SmallIntegerField(default=0)
    Genre = models.CharField(max_length=20)
    Publisher = models.CharField(max_length=20)
    NA_Sales = models.FloatField(default=0.0)
    EU_Sales = models.FloatField(default=0.0)
    JP_Sales = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
    Other_Sales = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
    Global_Sales = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)