from drf_yasg.utils import swagger_auto_schema
from .serializers import UserSerializer
from .tasks import *
from rest_framework.views import APIView
from rest_framework.response import Response

class CreateUserAPI(APIView):
    # Метод для создания пользователя
    @swagger_auto_schema(responses={200: "success"}, query_serializer=UserSerializer)
    def post(self, request):
        create_user.delay(request.data) # создание пользователя делегируется на сервис авторизации через брокер сообщений
        return Response()
