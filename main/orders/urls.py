from django.urls import path

from orders.views import *

urlpatterns = [
    path('', MakeOrderApi.as_view()),
]