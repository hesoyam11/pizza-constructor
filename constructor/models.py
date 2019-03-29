from decimal import Decimal
from datetime import datetime
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


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
    price = models.DecimalField(max_digits=8, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    pizza_order = models.ForeignKey(
        'PizzaOrder',
        related_name='ingredient_amounts',
        on_delete=models.PROTECT
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        related_name='ingredient_amounts',
        on_delete=models.SET_NULL,
        null=True
    )
    fixed_price = models.DecimalField(max_digits=8, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.01'))])
    amount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=1
    )

    def __str__(self):
        if self.ingredient:
            ingredient_name = self.ingredient.name
        else:
            ingredient_name = 'Unknown'
        return ', '.join([ingredient_name, str(self.amount), '{:.2f}'.format(self.fixed_price)])


class PizzaOrder(models.Model):
    BLACK = 'B'
    WHITE = 'W'

    DOUGH_CHOICES = (
        (BLACK, 'Black'),
        (WHITE, 'White')
    )

    INVALID_PHONE_MESSAGE = "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    PHONE_REGEX = RegexValidator(regex=r'^\+?\d{9,15}$', message=INVALID_PHONE_MESSAGE)

    ingredients = models.ManyToManyField(
        'Ingredient',
        through=IngredientAmount,
        related_name='pizza_orders'
    )
    dough = models.CharField(max_length=1, choices=DOUGH_CHOICES, default=WHITE)
    customer_name = models.CharField(max_length=64)
    phone_number = models.CharField(validators=[PHONE_REGEX], max_length=16)
    email = models.EmailField()
    order_price = models.DecimalField(max_digits=8, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.01'))])
    date_created = models.DateTimeField(default=datetime.now)
    date_confirmed = models.DateTimeField(null=True)

    def __str__(self):
        return ', '.join([self.customer_name, self.email, '{:.2f}'.format(self.order_price)])
