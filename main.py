import requests
import os
from dotenv import load_dotenv
from time import sleep
import telegram


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
            if response.json()["status"] == 'timeout':
                timestamp = response.json()["timestamp_to_request"]
            elif response.json()["status"] == 'found':
                bot = telegram.Bot(token=os.environ['TLG_TOKEN'])
                chat_id = os.environ['TLG_CHAT_ID']
                lesson = response.json()['new_attempts'][0]['lesson_title']
                lesson_url = response.json()['new_attempts'][0]['lesson_url']
                if response.json()['new_attempts'][0]['is_negative']:
                    send_message = bot.send_message(chat_id=chat_id,
                                                    text=f"Hello. Преподаватель проверил работу!\n"
                                                         f"Урок: {lesson}"
                                                         f"\n{lesson_url}\n"
                                                         f"К сожалению в работе нашлись ошибки")
                else:
                    send_message = bot.send_message(chat_id=chat_id,
                                                    text=f"Hello, Evgen. Преподаватель проверил работу!\n"
                                                         f"Урок: {lesson}\n"
                                                         f"Преподавателю всё понравилось, "
                                                         f"можно приступать к следующему уроку")
                timestamp = response.json()["last_attempt_timestamp"]
            else:
                timestamp = response.json()["timestamp"]
        except requests.exceptions.ConnectionError:
            sleep(5)
            pass
        except requests.exceptions.ReadTimeout:
            pass


if __name__ == '__main__':
    print(main())
