from statistics import fmean

import pandas as pd
from django.db.models import QuerySet


# Группирует данные базы данных по моделям роботов, чтобы распространить их на конкретные страницы файла таблиц
def group_into_models(queryset: QuerySet):
    models_set = {}
    for rec in queryset:
        rename_keys(rec)
        if rec['Модель'] not in models_set.keys():
            models_set[rec['Модель']] = [rec]
        else:
            models_set[rec['Модель']].append(rec)
    return models_set

# Переименовывает ключи для группированных данных QuerySet
def rename_keys(rec):
    rec['Модель'] = rec.pop('model')
    rec['Версия'] = rec.pop("version")
    rec['Количество за неделю'] = rec.pop("total")

# Создаем фреймы для каждой модели роботаС
def get_frames_list(frame_data: dict):
    frames_list = []
    for key in frame_data.keys():
        frames_list.append((key, pd.DataFrame(frame_data[key])))
    return frames_list