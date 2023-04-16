class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    H_IN_MIN = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    run_coeff_1 = 18
    run_coeff_2 = 20

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal_run = self.run_coeff_1 * self.get_mean_speed() - self.run_coeff_2
        return (cal_run * self.weight / self.M_IN_KM
                * self.duration * self.H_IN_MIN)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    M_IN_KM = 1000
    LEN_STEP = 0.65
    walk_coeff_1 = 0.035
    walk_coeff_2 = 2
    walk_coeff_3 = 0.029

    def __init__(self, action: int,
                 duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal_wlk_1 = self.walk_coeff_1 * self.weight
        cal_wlk_2 = self.get_mean_speed() ** self.walk_coeff_2 // self.height
        cal_wlk_3 = cal_wlk_1 + cal_wlk_2 * self.walk_coeff_3 * self.weight
        return cal_wlk_3 * self.duration * self.H_IN_MIN


class Swimming(Training):
    """Тренировка: плавание."""

    M_IN_KM = 1000
    LEN_STEP = 1.38
    swim_coeff_1 = 1.1
    swim_coeff_2 = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed_swm = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)
        return mean_speed_swm

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        cal_swm = (
            (self.get_mean_speed() + self.swim_coeff_1)
            * self.swim_coeff_2 * self.weight * self.duration)
        return cal_swm


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout: dict[str, type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
