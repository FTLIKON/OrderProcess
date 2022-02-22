from django.db import models


class orders(models.Model):
    orderId = models.IntegerField()
    orderTime = models.IntegerField()
    skuId = models.IntegerField()
    userId = models.IntegerField()
    status = models.IntegerField()
    price = models.FloatField(max_length=15)
    pay = models.FloatField(max_length=15)
