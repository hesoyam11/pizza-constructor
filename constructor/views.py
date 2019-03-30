from django.shortcuts import render
from .models import IngredientGroup


def pizza_construct(request):
    if request.method == 'POST':
        print('POST detected!')
        for k, v in request.POST.items():
            print(k, v)

    groups = IngredientGroup.objects.all()

    return render(
        request,
        'constructor/pizza_constructor.html',
        {
            'groups': groups
        }
    )
