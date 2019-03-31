from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import IngredientGroup, Ingredient, IngredientAmount
from .forms import PizzaOrderForm


def pizza_construct(request):
    groups = IngredientGroup.objects.all()
    ingredients = Ingredient.objects.all()

    if request.method == 'POST':
        pizza_order_form = PizzaOrderForm(request.POST)

        if not pizza_order_form.is_valid():
            return render(
                request,
                'constructor/pizza_constructor.html',
                {
                    'groups': groups,
                    'form': pizza_order_form
                }
            )

        order_price = Decimal(0)
        amounts = []

        for ingredient in ingredients:
            if str(ingredient.id) in request.POST:
                try:
                    amount = int(request.POST[str(ingredient.id)])
                    if not 0 <= amount <= 100:
                        raise ValueError
                except ValueError:
                    return HttpResponseBadRequest(
                        content='Invalid ingredient amount format.'
                    )
                if amount > 0:
                    order_price += ingredient.price * Decimal(amount)
                    amounts.append(IngredientAmount(
                        fixed_price=ingredient.price,
                        amount=amount,
                        ingredient=ingredient
                    ))

        if str(order_price) != request.POST['order_price']:
            return HttpResponseBadRequest(
                content='Client-side order price is outdated.'
            )

        pizza_order = pizza_order_form.save()
        for ingredient_amount in amounts:
            ingredient_amount.pizza_order = pizza_order
            ingredient_amount.save()

        return render(
            request,
            'constructor/order_confirmation.html',
            {
                'email': pizza_order.email
            }
        )

    return render(
        request,
        'constructor/pizza_constructor.html',
        {
            'groups': groups
        }
    )
