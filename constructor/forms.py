from django.forms import ModelForm
from .models import PizzaOrder


class PizzaOrderForm(ModelForm):
    class Meta:
        model = PizzaOrder
        fields = ('dough', 'customer_name', 'phone_number', 'email', 'order_price')
