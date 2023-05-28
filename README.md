# Телеграм Бот для оповещениях о проверенных работах на dvmn.org
 Бот использует API dvmn.org

## Описание
С помощью данного бота можно напоминать себе о проверенных заданиях с сайта dvmn.org

## Требования
Для работы должен быть установлен python3. А также необходимо установить библиотеки requests, python-dotenv, 
python-telegram-bot==13.15. 
Чтобы установить python3 скачайте и ознакомьтесь с инструкцией по установке на сайте [python.org](https://www.python.org/downoloads)

## Установка
Библиотека requests устанавливается командой:
```bash
pip install requests
```

Библиотека python-dotenv устанавливается командой:
```bash
pip install python-dotenv
```
Библиотека python-telegram устанавливается командой:
```bash
pip install python-telegram-bot==13.15
```

## Настройки
Необходимо чтобы в дирректории проекта был файл .env, в котором содержаться переменные окружения:
* DEVMAN_TOKEN - узнать можно в профиле на [https://dvmn.org/api/docs/]
* TLG_CHAT_ID - id чата с ботом. Узнать можно написав @userinfobot
* TLG_TOKEN - токен телеграм бота, узнать можно у @BotFather

## Пример запуска скрипта
```bash
python main.py
```
