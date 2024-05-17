import logging
from datetime import datetime, timedelta

from celery import shared_task

from habit.models import Habit
from habit.services import create_telegram_message

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_task():
    habits = Habit.objects.filter(period='Каждый день')
    for habit in habits:
        time_max = datetime.now() + timedelta(seconds=30)
        time_min = datetime.now() - timedelta(seconds=30)
        if time_min.time() <= habit.time <= time_max.time():
            create_telegram_message(habit)


@shared_task
def send_telegram_task_weekly():
    habits = Habit.objects.filter(period='Раз в неделю')

    for habit in habits:

        current_date = datetime.now()
        if habit.updated_time is None:
            create_telegram_message(habit)
            habit.updated_time = current_date + timedelta(days=7)
            habit.save()
        else:

            time_max = datetime.now() + timedelta(seconds=30)
            time_min = datetime.now() - timedelta(seconds=30)
            if current_date.date() == habit.updated_time.date():
                if (time_min.time() <=
                        habit.updated_time.time() <=
                        time_max.time()):
                    create_telegram_message(habit)
                    habit.updated_time = (
                            current_date +
                            timedelta(days=7))
                    habit.save()


@shared_task
def send_telegram_several_task():
    habits = Habit.objects.filter(
        period='Несколько дней'
    )

    for habit in habits:

        current_date = datetime.now()
        if habit.updated_time is None:
            create_telegram_message(habit)
            habit.updated_time = (
                    current_date +
                    timedelta(days=2))
            habit.save()
        else:

            time_max = (datetime.now() +
                        timedelta(seconds=30))
            time_min = (datetime.now() -
                        timedelta(seconds=30))
            if (current_date.date() ==
                    habit.updated_time.date()):
                if (time_min.time() <=
                        habit.updated_time.time() <=
                        time_max.time()):
                    create_telegram_message(habit)
                    habit.updated_time = (
                            current_date +
                            timedelta(days=2))
                    habit.save()
