from django.urls import path
from . import views


urlpatterns = [
    path('', views.pizza_construct,
         name='pizza_construct')
]
