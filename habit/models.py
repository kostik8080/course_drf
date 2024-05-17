from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}

PERIOD_CHOICES = (
    ('Каждый день', 'Every Day'),
    ('Несколько дней', 'Some Days'),
    ('Раз в неделю', 'Every Week'),

)


class Habit(models.Model):
    """Модель привычки"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        **NULLABLE
    )
    pleasant_habit = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name='связаная привычка',
        **NULLABLE
    )  # Пользователь, создавший привычку
    place = models.CharField(
        max_length=255,
        verbose_name='Место',
        **NULLABLE
    )
    time = models.TimeField(
        verbose_name='Время',
        **NULLABLE
    )
    action = models.TextField(verbose_name='Действие')
    period = models.CharField(
        max_length=255,
        choices=PERIOD_CHOICES,
        verbose_name='Период',
        default='Каждый день'
    )
    award = models.TextField(
        verbose_name='Награда',
        **NULLABLE
    )
    time_to_complete = models.TimeField(
        verbose_name='Время на выполнение',
        **NULLABLE
    )
    sign_pleasand_habit = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    public = models.BooleanField(
        default=False,
        verbose_name='Опубликовать'
    )
    updated_time = models.DateTimeField(
        verbose_name='Последнее уведомление',
        **NULLABLE
    )
