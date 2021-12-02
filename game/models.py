from django.db import models

# Create your models here.
class Game_sale(models.Model):
    name = models.CharField(max_length=200)
    Platform = models.CharField(max_length=10)
    year = models.SmallIntegerField(default= 0)
    genre =  models.CharField(max_length=20)
    Publisher = models.CharField(max_length=20)
    NA_Sales = models.DecimalField(max_digits=6, decimal_places=3,default= 0.0)
    EU_Sales = models.DecimalField(max_digits=6, decimal_places=3,default= 0.0)
    JP_Sales = models.DecimalField(max_digits=6, decimal_places=3,default= 0.0)
    Other_Sales = models.DecimalField(max_digits=6, decimal_places=3,default= 0.0)
    Global_Sales = models.DecimalField(max_digits=6, decimal_places=3,default= 0.0)