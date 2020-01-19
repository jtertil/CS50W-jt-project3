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
    name = models.CharField(max_length=64)
    size = models.ForeignKey(MealSize, null=True, blank=True, on_delete=models.CASCADE)
    type = models.ForeignKey(MealType, on_delete=models.CASCADE)
    extra_ingredients = models.PositiveIntegerField(default=0)
    available_ingredients = models.ManyToManyField(Ingredient, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} - {self.price}$ '



