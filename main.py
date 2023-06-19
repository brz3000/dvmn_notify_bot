import requests
import os
from dotenv import load_dotenv
from time import sleep
import telegram
from textwrap import dedent
import logging


logger = logging.getLogger('new_logger')


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    load_dotenv()
    chat_id = os.environ['TLG_CHAT_ID']
    bot_logger = telegram.Bot(token=os.environ['TLG_TOKEN_LOGGER_BOT'])
    logger.setLevel(logging.DEBUG)
    logger.addHandler(TelegramLogsHandler(bot_logger, chat_id))
    logger.info('Бот запущен')
    token = os.environ['DEVMAN_TOKEN']
    headers = {"Authorization": f'Token {token}'}
    timestamp = ''
    params = {"timestamp": timestamp}
    url = 'https://dvmn.org/api/long_polling/'

    while True:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            reviews = response.json()
            if reviews["status"] == 'timeout':
                timestamp = reviews["timestamp_to_request"]
            elif reviews["status"] == 'found':
                bot = telegram.Bot(token=os.environ['TLG_TOKEN_NOTIFY_BOT'])
                chat_id = os.environ['TLG_CHAT_ID']
                lesson = reviews['new_attempts'][0]['lesson_title']
                lesson_url = reviews['new_attempts'][0]['lesson_url']
                if reviews['new_attempts'][0]['is_negative']:
                    send_message = bot.send_message(chat_id=chat_id,
                                                    text=dedent(f'''Hello.
                                                    Преподаватель проверил работу!
                                                    Урок: {lesson}.
                                                    {lesson_url}.
                                                    К сожалению в работе нашлись ошибки'''))
                else:
                    send_message = bot.send_message(chat_id=chat_id,
                                                    text=dedent(f'''Hello.
                                                    Преподаватель проверил работу!
                                                    Урок: {lesson}
                                                    Преподавателю всё понравилось,
                                                    можно приступать к следующему уроку'''))
                timestamp = reviews["last_attempt_timestamp"]
        except requests.exceptions.ConnectionError:
            sleep(5)
        except requests.exceptions.ReadTimeout:
            pass
        except Exception as err:
            logger.error("Бот упал с ошибкой:")
            logger.error(err, exc_info=True)
            sleep(50)


if __name__ == '__main__':
    main()
