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

    available_toppings = models.ManyToManyField(PizzaTopping)
    toppings_amount = models.IntegerField(
        choices=TOPPINGS_AMOUNT_CHOICES,
        default=0
    )
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.type} {self.get_toppings_amount_display()} {self.size} - {self.cost}$'


class SubExtra(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class Sub(models.Model):
    name = models.CharField(max_length=32)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    max_extras = models.PositiveIntegerField(default=1)
    available_extras = models.ManyToManyField(SubExtra)

    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} {self.size} - {self.cost}$'


class Pasta(models.Model):
    name = models.CharField(max_length=32)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.cost}$'


class Salad(models.Model):
    name = models.CharField(max_length = 32)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.cost}$'


class DinnerPlatters(models.Model):
    name = models.CharField(max_length=32)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} {self.size} - {self.cost}$'
