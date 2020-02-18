from django.db import models


class MealSize(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class MealType(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.name}'


class Meal(models.Model):
    type = models.ForeignKey(
        MealType, on_delete=models.CASCADE)
    size = models.ForeignKey(
        MealSize, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    is_special = models.BooleanField(default=False)
    num_of_toppings = models.PositiveIntegerField(default=0)
    available_toppings = models.ManyToManyField(
        Ingredient, related_name='toppings', blank=True)

    num_of_extras = models.PositiveIntegerField(default=0)
    available_extras = models.ManyToManyField(
        Ingredient, related_name='extras', blank=True)
    extras_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True)

    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}$ '



