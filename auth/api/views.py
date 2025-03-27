from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg import openapi
from rest_framework.decorators import api_view

class UserView(APIView):

    # Создание пользователя
    @swagger_auto_schema(responses={
        200: openapi.Response(
            description="Успешный ответ",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
                },
            ),
        ),
    }, query_serializer=UserSerializer)
    def post(self, request):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user_obj = user.save()
        token_data = RefreshToken.for_user(user_obj)
        refresh, access = str(token_data), str(token_data.access_token)
        return Response(status=200, data={"refresh": refresh, "access": access})

# Авторизация пользователя
@swagger_auto_schema(
    responses={
        200: openapi.Response(
            description="Успешный ответ",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID пользователя'),
                },
            ),
        ),
    }
,method="POST")
@api_view(['POST'])
def auth(request):
    return Response(data={"user": request.user.pk})