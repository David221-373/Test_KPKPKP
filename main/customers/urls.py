from .views import *
from django.urls import path

urlpatterns = [
    path("create", CreateUserAPI.as_view())
]
