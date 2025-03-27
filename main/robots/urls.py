
from django.urls import path, include
from .views import *

urlpatterns = [
    path("table", export_excel),
    path("", RobotView.as_view())
]
