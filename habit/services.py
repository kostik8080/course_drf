import requests
import logging
from config import settings

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
    message = (f'Привет тебе, пора {habit.action}'
               f' в {habit.place}.'
               f'Ты сам захотел это сделать'
               f' в {habit.place}.'
               f'И давай не забывай, тебе всего надо'
               f' на это {habit.time_to_complete} минут.')
    send_telegram(settings.TELEGRAM_CHAT_ID, message)
    logger.info(f"Уведомление {message} отправлено")
