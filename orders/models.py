from django.db import models


class Size(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Extra(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Type(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=300, null=True, blank=True)
    extras_name = models.CharField(max_length = 50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(max_length=100)
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

    def __str__(self):
        return f'{self.name} - {self.base_price}$'
