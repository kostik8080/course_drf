import requests
import logging

from django.db.models import Q

from config import settings
from users.models import User

logger = logging.getLogger(__name__)


def send_telegram(chat_id, message):
    PARAMS = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(
        f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage',
        params=PARAMS
    )


def create_telegram_message(habit):
    try:
        user = User.objects.get(Q(email=habit.user.email))
        chat_id = user.chat_id
        if chat_id:
            message = (f'Привет тебе, пора {habit.action}'
                       f' в {habit.place}.'
                       f'Ты сам захотел это сделать'
                       f' в {habit.place}.'
                       f'И давай не забывай, тебе всего надо'
                       f' на это {habit.time_to_complete} минут.')
            send_telegram(chat_id, message)
            logger.info(f"Уведомление {message} отправлено")
    except User.DoesNotExist:
        logger.info(f"Пользователь с email {habit.user.email} не найден")


