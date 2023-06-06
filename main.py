import requests
import os
from dotenv import load_dotenv
from time import sleep
import telegram
from textwrap import dedent
import logging


logging.basicConfig(level=logging.DEBUG)
logging.debug('Сообщение уровня DEBUG')


def main():
    load_dotenv()
    token = os.environ['DEVMAN_TOKEN']
    headers = {"Authorization": f'Token {token}'}
    timestamp = ''
    params = {"timestamp": timestamp}
    url = 'https://dvmn.org/api/long_polling/'

    while True:
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            answer_from_api_devman = response.json()
            if answer_from_api_devman["status"] == 'timeout':
                timestamp = answer_from_api_devman["timestamp_to_request"]
            elif answer_from_api_devman["status"] == 'found':
                bot = telegram.Bot(token=os.environ['TLG_TOKEN'])
                chat_id = os.environ['TLG_CHAT_ID']
                lesson = answer_from_api_devman['new_attempts'][0]['lesson_title']
                lesson_url = answer_from_api_devman['new_attempts'][0]['lesson_url']
                if answer_from_api_devman['new_attempts'][0]['is_negative']:
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
                timestamp = answer_from_api_devman["last_attempt_timestamp"]
        except requests.exceptions.ConnectionError:
            sleep(5)
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    main()
