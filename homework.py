class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Возвращаем строку сообщения."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    W_T_IN_MIN = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        report = InfoMessage(self.__class__.__name__, self.duration,
                             self.get_distance(), self.get_mean_speed(),
                             self.get_spent_calories())
        return report


class Running(Training):
    """Тренировка: бег."""
    factor_1: float = 18
    factor_2: float = 20

    def _init_(self,
               action: int,
               duration: float,
               weight: float,
               speed: float,
               calories: float
               ) -> None:
        super().__init__(action, duration, weight)
        self.speed = speed
        self.calories = calories

    def get_spent_calories(self) -> float:
        desired_value_1 = ((self.factor_1 * self.get_mean_speed()
                            - self.factor_2) * self.weight)
        return (desired_value_1 / self.M_IN_KM) * (self.duration * self.W_T_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    factor_3: float = 0.035
    degree: float = 2
    factor_4: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        desired_value_3 = (self.factor_3 * self.weight)
        desired_value_4 = (self.get_mean_speed()**self.degree // self.height)
        desired_value_5 = (self.factor_4 * self.weight)
        sportsWalking_calories = (desired_value_3
                                  + (desired_value_4 * desired_value_5)
                                  ) * self.duration * self.W_T_IN_MIN
        return sportsWalking_calories


class Swimming(Training):
    """Тренировка: плавание."""
    factor_5: float = 1.1
    factor_6: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        swimming_calories = ((self.get_mean_speed()
                             + self.factor_5) * self.factor_6 * self.weight)
        return swimming_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: dict = {'SWM': Swimming,
                        'RUN': Running,
                        'WLK': SportsWalking}
    return dictionary[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)

        if training is None:
            print('Неожиданный тип тренировки')
        else:
            main(training)
