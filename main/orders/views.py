from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from robots.models import *
from .models import *
from .serializers import OrderSerializer


class MakeOrderApi(APIView):
    permission_classes = (IsAuthenticated, ) # этим методом не может пользоваться неавторизованный пользователь

    # Метод для создания заказа
    @swagger_auto_schema(responses={200: "success"}, query_serializer=OrderSerializer)
    def post(self, request):
       user, serial, is_waiting = request.user, request.data.get('robot_serial'), False
       if not Robot.objects.filter(serial=serial):
           is_waiting = True
       Order.objects.create(customer=user, robot_serial=serial, in_waiting=is_waiting)
       return HttpResponse()