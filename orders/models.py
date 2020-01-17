from django.db import models


class PizzaTopping(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class Size(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class PizzaType(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Pizza(models.Model):
    TOPPINGS_AMOUNT_CHOICES = [
        (0, 'cheese only'),
        (1, '1 topping'),
        (2, '2 toppings'),
        (3, '3 toppings'),
        (5, 'special')
    ]

    type = models.ForeignKey(PizzaType, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    toppings_amount = models.IntegerField(
        choices=TOPPINGS_AMOUNT_CHOICES,
        default=0
    )
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.size} {self.type}' \
               f' {self.get_toppings_amount_display()} - {self.cost}$'
