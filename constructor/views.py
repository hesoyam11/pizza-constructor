from django.shortcuts import render
from .models import IngredientGroup


def pizza_construct(request):
    if request.method == 'POST':
        print('POST detected!')

    groups = IngredientGroup.objects.all()

    return render(
        request,
        'constructor/pizza_constructor.html',
        {
            'groups': groups
        }
    )
