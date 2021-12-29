from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    REPORT: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить информацию о тренировке."""
        return self.REPORT.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        report: InfoMessage = InfoMessage(self.__class__.__name__,
                                          self.duration,
                                          self.get_distance(),
                                          self.get_mean_speed(),
                                          self.get_spent_calories())
        return report


class Running(Training):
    """Тренировка: бег."""

    COEFF_CAL_RUN_1: float = 18
    COEFF_CAL_RUN_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        desired_value_1: float = ((self.COEFF_CAL_RUN_1 * self.get_mean_speed()
                                   - self.COEFF_CAL_RUN_2) * self.weight)
        desired_value_2: float = (self.duration * self.MIN_IN_H)
        return (desired_value_1 / self.M_IN_KM) * desired_value_2


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CAL_WLK_1: float = 0.035
    COEFF_CAL_WLK_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        desired_value_3: float = (self.COEFF_CAL_WLK_1 * self.weight)
        desired_value_4: float = (self.get_mean_speed() ** 2 // self.height)
        desired_value_5: float = (self.COEFF_CAL_WLK_2 * self.weight)
        sports_walking_calories: float = (desired_value_3
                                          + (desired_value_4 * desired_value_5)
                                          ) * self.duration * self.MIN_IN_H
        return sports_walking_calories


class Swimming(Training):
    """Тренировка: плавание."""

    COEFF_CAL_SWM_1: float = 1.1
    COEFF_CAL_SWM_2: float = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        desired_value_6: float = self.length_pool * self.count_pool
        return desired_value_6 / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        swimming_calories: float = ((self.get_mean_speed()
                                     + self.COEFF_CAL_SWM_1)
                                    ) * self.COEFF_CAL_SWM_2 * self.weight
        return swimming_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dictionary: dict[str, type] = {'SWM': Swimming,
                                   'RUN': Running,
                                   'WLK': SportsWalking}
    return dictionary[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
