from datetime import time

from rest_framework.serializers import ValidationError


class Hobit_Plese_Useful_Validator:
    """Валидатор, проверяющий, что пользователь
       не может использовать
       сразу вознаграждения и связанную привычку.
     """

    def __init__(self, pleasant_habit, award):
        self.pleasant_habit = pleasant_habit
        self.award = award

    def __call__(self, value):
        tmp_pleasant_habit = dict(value).get(self.pleasant_habit)
        tmp_award = dict(value).get(self.award)
        if tmp_pleasant_habit is not None and tmp_award is not None:
            raise ValidationError(
                'Вы не можете использовать'
                ' два значения вознаграждения '
                'и связанную привычку')


class Time_Validator:
    """Волидатор проверяющий,
       что время выполнения
       не может быть больше 2 минут.
    """

    def __init__(self, time_to_complete):
        self.time_to_complete = time_to_complete

    def __call__(self, value):
        time_minutes = time(
            hour=0,
            minute=2,
            second=0)
        tmp_time = dict(value).get(self.time_to_complete)
        if tmp_time is not None:

            if tmp_time > time_minutes:
                raise ValidationError(
                    'Время выполнения'
                    ' не может быть больше 2 минут')


class Related_Sign_Validator:
    """Валидатор для проверки,
       является ли
       связанная привычка приятной
    """

    def __init__(self, pleasant_habit):
        self.pleasant_habit = pleasant_habit

    def __call__(self, value):
        pleasant = dict(value).get(self.pleasant_habit)

        if pleasant:
            if not pleasant.sign_pleasand_habit:
                raise ValidationError(
                    'В связанные привычки'
                    ' могут попадать только привычки'
                    ' с приятным признаком.')


class Good_Sign_Validator:
    """Валидатор проверяющий,
       что у приятной привычки
       не может быть вознаграждения
       или связанной привычки
    """

    def __init__(self, pleasant_habit, sign_pleasand_habit, award):
        self.pleasant_habit = pleasant_habit
        self.sign_pleasand_habit = sign_pleasand_habit
        self.award = award

    def __call__(self, value):
        pleasant = dict(value).get(self.pleasant_habit)
        sign = dict(value).get(self.sign_pleasand_habit)
        award = dict(value).get(self.award)
        if sign and (pleasant or award):
            raise ValidationError(
                'У приятной привычки'
                ' не может быть вознаграждения'
                ' или связанной привычки.')


class Priority_Validator:
    """Валидатор проверяющий,
       что поле priorid не может быть пустым.
    """
    def __init__(self, period):
        self.period = period

    def __call__(self, value):
        priority = dict(value).get(self.period)
        if priority is None:
            raise ValidationError(
                'Поле preriod не может быть пустым.'
                'Выбирите из вариантов'
                'Каждый день, Несколько дней, Раз в неделю')
