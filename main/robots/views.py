from django.db.models import Count
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated

from .models import *
from rest_framework.views import APIView

from .serializers import RobotSerializer
from .validation import *
import json
from .services import *
from io import BytesIO
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response

# Выгрузка excel отчёта
def export_excel(request):
    now = timezone.now() # определяем сегодняшнюю дату
    # выгружаем из базы данных всех роботов,
    # которые были созданы в течение недели и объединяем их по полю model,
    # а также считаем количество созданных версий модели
    robots = Robot.objects.filter(created__gte=now - timedelta(days=7)).values("model", "version").annotate(total=Count('version'))
    grouped_data = group_into_models(robots)
    frames_list = get_frames_list(grouped_data)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        for frame in frames_list:
            frame[1].to_excel(writer, sheet_name=frame[0])
    buffer.seek(0)
    # записываем данные excel в буфер, переводим указатель на ноль, чтобы читался весь файл и передаем файл из буффера в тело ответа
    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="robots.xlsx"'
    return response


class RobotView(APIView):
    permission_classes = (IsAuthenticated, )

    # Метод для создания робота
    @swagger_auto_schema(responses={200: "success"}, query_serializer=RobotSerializer)
    def post(self, request):
        data = json.loads(request.body)
        RobotCreateValidator(**data)
        data['serial'] = f"{data['model']}-{data['version']}"
        Robot.objects.create(**data)
        return Response(data="success")

