import time
import random

CIRCUIT_BREAKER_BAN_TIME = 1 * 60  # 1 min
CIRCUIT_BREAKER_CONNECT_CHANCE = 25
CIRCUIT_BREAKER_CONNECT_TRIES = 5


class CircuitBreaker:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(CircuitBreaker, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.requests_data = {}

    def try_connect(self, service_name):
        # добавление нового сервиса в circuit braker для отслеживания доступности сервиса
        # (закрытое состояние, запрос разрешен)
        if service_name not in self.requests_data.keys():
            self.requests_data[service_name] = [0, time.time()]
            return True
        # данный сервис уже отслеживается circuit braker
        else:
            # проверка на превышение лимита неудачных запросов к сервису
            if self.requests_data[service_name][0] == -1:
                # открытое состояние (запрос к сервису не разрешен)
                if self.requests_data[service_name][1] > time.time():
                    return False
                else:
                    # полуоткрытое состояние (некоторые запросы к сервису разрешаются,
                    # некоторые нет - ограниченный режим работы сервиса)
                    if random.randint(0, 100) >= CIRCUIT_BREAKER_CONNECT_CHANCE:
                        return False
        # закрытое состояние circuit braker (запрос к сервису разрешен)
        return True

    def connection_error(self, service_name):
        # переход из полуоткрытого в открытое состояние circuit braker
        if self.requests_data[service_name][0] == -1:
            self.requests_data[service_name][1] = time.time() + CIRCUIT_BREAKER_BAN_TIME
            return

        # увеличение счетчика неудачных попыток обращения к целевому сервису
        self.requests_data[service_name][0] += 1

        # если превышен лимит неудачных запросов к сервису,
        # то переходим из закрытого в открытое состояние circuit braker
        if self.requests_data[service_name][0] >= CIRCUIT_BREAKER_CONNECT_TRIES:
            self.requests_data[service_name][0] = -1
            self.requests_data[service_name][1] = time.time() + CIRCUIT_BREAKER_BAN_TIME

    def connection_successful(self, service_name):
        # сброс счетчика неудачных запросов к сервису после каждого удачного
        self.requests_data[service_name][0] = 0
