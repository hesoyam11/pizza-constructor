from django.db import models


class IngredientGroup(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    group = models.ForeignKey(
        'constructor.IngredientGroup',
        related_name='ingredients',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
