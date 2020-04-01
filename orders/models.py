from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
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
    description = models.CharField(max_length=300, null=True, blank=True)
    extras_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Item(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(
        Type, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size, null=True, blank=True, on_delete=models.CASCADE)
    extras_available = models.ManyToManyField(
        Extra, blank=True, related_name='items', symmetrical=False)
    extras_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0,
        validators=[MinValueValidator(0)])
    is_special = models.BooleanField(default=False)
    extras_max_quantity = models.PositiveIntegerField(default=0)
    base_price = models.DecimalField(
        max_digits=6, decimal_places=2,
        validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.name} - {self.base_price}$'

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)

        if float(self.extras_price) < 0:
            raise ValueError(f'Must be a value greater than or equal to 0')

        if float(self.base_price) < 0:
            raise ValueError(f'Must be a value greater than or equal to 0')


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete?
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  # on_delete?
    extras_selected = models.ManyToManyField(
        Extra, blank=True, related_name='baskets', symmetrical=False,
    )
    special_info = models.CharField(max_length=300, null=True, blank=True)

    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        indexes = [models.Index(fields=['user'])]

    def __str__(self):
        return f'{self.item.name} - {self.price}$'

    def save(self, *args, **kwargs):
        super(Basket, self).save(*args, **kwargs)

        if float(self.price) < 0:
            raise ValueError(f'Must be a value greater than or equal to 0')

        if self.extras_selected.count() > self.item.extras_max_quantity:
            raise ValueError(
                f'Max quantity of extras: {self.item.extras_max_quantity}')

        for e in self.extras_selected.values():
            if e not in self.item.extras_available.values():
                raise ValueError(
                  f'{e} not in item available extras'
                )

    def as_dict(self):
        return {
            'id': self.pk,
            'item': self.item.name,
            'extras_name': self.item.type.extras_name,
            'extras_selected': [e.name for e in self.extras_selected.all()],
            'special_info': self.special_info,
            'price': float(self.price)
        }


class Order(models.Model):
    def __str__(self):
        return f'order #{self.pk}'

    value = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # on_delete?
    data = JSONField()
    status = models.CharField(
        max_length = 1,
        choices = [('1', 'New'), ('2', 'Accepted'), ('3', 'Ready')],
        default = '1'
    )


