from csv import reader
from datetime import datetime
from itertools import cycle
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accel_file = None
        self.gps_file = None
        self.accel_reader = None
        self.gps_reader = None
        self.accel_cycle = None
        self.gps_cycle = None

    def read(self) -> AggregatedData:
        try:
            while True:
                accel_data = next(self.accel_reader)
                gps_data = next(self.gps_reader)

                # Пропускаємо перший рядок (заголовок)
                if accel_data[0].lower() == 'x' or gps_data[0].lower() == 'longitude':
                    continue

                # Перевірка, чи всі дані можна конвертувати в числа
                try:
                    accel_values = list(map(float, accel_data))
                    gps_values = list(map(float, gps_data))
                except ValueError:
                    raise ValueError("Invalid data format in accelerometer or gps file")

                # Перевірка, чи всі дані є числовими
                if not all(map(lambda x: isinstance(x, (int, float)), accel_values)) or not all(
                        map(lambda x: isinstance(x, (int, float)), gps_values)):
                    raise ValueError("Invalid data format in accelerometer or gps file")

                # Створення об'єктів прискорення та GPS
                accelerometer = Accelerometer(x=int(accel_values[0]), y=int(accel_values[1]), z=int(accel_values[2]))
                gps = Gps(longitude=float(gps_values[0]), latitude=float(gps_values[1]))

                # Повернення об'єкту AggregatedData
                return AggregatedData(accelerometer=accelerometer, gps=gps, timestamp=datetime.now(), user_id=1)
        except StopIteration:
            self.startReading()  # Почати зчитування з початку файлу
            return self.read()  # Повернення даних з початку файлу

    def startReading(self, *args, **kwargs):
        self.accel_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')

        self.accel_reader = iter(reader(self.accel_file))
        self.gps_reader = iter(reader(self.gps_file))

    def stopReading(self, *args, **kwargs):
        if self.accel_file:
            self.accel_file.close()
        if self.gps_file:
            self.gps_file.close()
