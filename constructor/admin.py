from django.contrib import admin
from constructor.models import IngredientGroup, Ingredient, IngredientAmount, PizzaOrder

admin.site.register(IngredientGroup)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(PizzaOrder)
