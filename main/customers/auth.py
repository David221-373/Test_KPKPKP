
from rest_framework import authentication
import requests
from R4C.settings import AUTH_SERVICE_URL
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User, AnonymousUser

# Аутентификация делегируется на сервис авторизации
class Auth(authentication.BaseAuthentication):
    def authenticate(self, request):
        req = requests.Request
        token = request.headers.get('Authorization')
        if token is None: # если токен не дан пользователем, значит он не производит попытку авторизации
            return None
        headers = {'Authorization': token} # если токен дан, записываем его в заголовок

        res = requests.post(url=f'{AUTH_SERVICE_URL}/auth', headers=headers) # производим запрос на авторизацию
        if res.status_code != 200:
            raise AuthenticationFailed("Service answered with error") # если авторизация провалилась, выбрасывается исключение
        return User.objects.get(pk=int(res.json()['user'])), None # если всё прошло хорошо, пользователь авторизуетсялс