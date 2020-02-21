from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class Extra(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class Type(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, null=True, blank=True)
    extras_name = models.CharField(max_length = 32, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size, null=True, blank=True, on_delete=models.CASCADE)
    extras_available = models.ManyToManyField(
        Extra, blank=True, related_name='items')
    extras_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0)

    is_special = models.BooleanField(default=False)
    extras_max_quantity = models.PositiveIntegerField(default=0)

    base_price = models.DecimalField(
        max_digits=6, decimal_places=2)


