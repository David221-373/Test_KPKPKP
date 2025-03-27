from celery import shared_task
import requests
from R4C import settings

# Задача по созданию пользователя, задействующая асинхронную очередь задачда
@shared_task
def create_user(user_data):
    requests.post(url=f'{settings.AUTH_SERVICE_URL}/create', data=user_data)