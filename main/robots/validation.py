from datetime import datetime
from R4C.exceptions import *
import re

# Валидирует пришедшие для создания робота данные
class RobotCreateValidator:
    VALIDATE_LIST = ['model', 'version', 'created'] # список валидируемых полей

    def __init__(self, **kwargs):
        if not all(item in kwargs.keys() for item in RobotCreateValidator.VALIDATE_LIST):
            raise InvalidInputData
        self.model = kwargs['model']
        self.version = kwargs['version']
        try:
            self.created = datetime.strptime(kwargs['created'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise InvalidInputData()
        self.validate_all()

    # валидирует все поля, указанные в VALIDATE_LIST
    def validate_all(self):
        for v_object in RobotCreateValidator.VALIDATE_LIST:
            self.__getattribute__(f'validate_{v_object}')()

    def validate_model(self):
        if isinstance(self.model, str) and len(self.model) != 2:
            raise InvalidModel()

    def validate_version(self):
        if not re.match(r"D\d+", self.version):
            raise InvalidVersion()

    def validate_created(self):
        if datetime.now() < self.created:
            raise InvalidDate()
