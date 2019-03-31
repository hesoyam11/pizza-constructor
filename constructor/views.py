from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import IngredientGroup, PizzaOrder
from .forms import PizzaOrderForm


def pizza_construct(request):
    groups = IngredientGroup.objects.all()

    if request.method == 'POST':
        try:
            # dough = request.POST['dough']
            # customer_name = request.POST['customer_name']
            # email = request.POST['email']
            # phone_number = request.POST['phone_number']
            pizza_order_form = PizzaOrderForm(request.POST)
        except KeyError:
            return HttpResponseBadRequest(
                content="One of the required params not specified."
            )

        # print(dough, customer_name, email, phone_number)
        if not pizza_order_form.is_valid():
            return render(
                request,
                'constructor/pizza_constructor.html',
                {
                    'groups': groups,
                    'form': pizza_order_form
                }
            )
        else:
            print('POST OK')

    return render(
        request,
        'constructor/pizza_constructor.html',
        {
            'groups': groups
        }
    )
