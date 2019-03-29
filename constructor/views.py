from django.shortcuts import render


def pizza_construct(request):
    return render(
        request,
        'constructor/pizza_constructor.html',
        {

        }
    )
