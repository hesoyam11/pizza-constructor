from decimal import Decimal
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseServerError
from django.utils import timezone
from django.utils.html import strip_tags
from smtplib import SMTPAuthenticationError
from .models import IngredientGroup, Ingredient, IngredientAmount, PizzaOrder
from .forms import PizzaOrderForm
from pizza_constructor.local_settings import EMAIL_HOST_USER


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

        current_site = get_current_site(request)
        mail_subject = 'Confirm your pizza order.'

        html_message = render_to_string('constructor/confirmation_letter.html', {
            'pizza_order': pizza_order,
            'domain': current_site.domain,
        })
        plain_message = strip_tags(html_message)

        try:
            mail.send_mail(
                mail_subject,
                plain_message,
                'Pizza Constructor {0}'.format(EMAIL_HOST_USER),
                [pizza_order.email],
                html_message=html_message
            )
        except SMTPAuthenticationError:
            pizza_order.delete()
            return HttpResponseServerError(
                content='An error occurred while sending email on the server.'
            )

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


def order_confirm(request, order_id, token):
    pizza_order = get_object_or_404(PizzaOrder, pk=order_id)

    if pizza_order.date_confirmed:
        return HttpResponse('The order is already confirmed.')

    if pizza_order.confirmation_token != token:
        return HttpResponseBadRequest('Confirmation link is invalid.')

    pizza_order.date_confirmed = timezone.now()
    pizza_order.save()
    return HttpResponse('Thank you for your email order confirmation.')
