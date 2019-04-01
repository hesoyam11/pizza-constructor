from django.urls import path
from . import views


urlpatterns = [
    path('', views.pizza_construct, name='pizza_construct'),
    path(
        'order/<int:order_id>/confirm/<slug:token>/',
        views.order_confirm, name='order_confirm'
    )
]
