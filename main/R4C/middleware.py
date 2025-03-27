from .exceptions import *
from django.http import HttpResponse
from django.middleware.common import MiddlewareMixin

# Middleware для обработки кастомных исключений
class HandleCustomExceptions(MiddlewareMixin):

    def process_exception(self, request, exception):
        if isinstance(exception, InvalidModel):
            return HttpResponse("Неправильно задана модель робота", status=400)
        if isinstance(exception, InvalidVersion):
            return HttpResponse("Неправильно задана версия робота", status=400)
        if isinstance(exception, InvalidDate):
            return HttpResponse("Неправильно задана дата создания робота", status=400)
        if isinstance(exception, InvalidInputData):
            return HttpResponse("Данные отправлены в недопустимом формате", status=400)