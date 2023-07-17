# mailing_statistics
Данный сервис отправляет пользователям сообщения, есть возможность запланировать время отправки.

## Установка:
- Скачать репрозиторий:
	- > git clone https://github.com/yonvik/mailing_statistics.git
- установить и активировать виртуальное окружение venv:
  - > python -m venv venv
  - > . venv/scripts/activate
- Установить зависимости :
  - > pip install -r requirements.txt
- Перейти в директорию:
  - > cd mailing_statistics
- Включить сервер:
  - > python manage.py runserver

# Примеры json запросов 
1. Добавление нового получателя:
URL: `/clients/`
Метод: `POST`
Тело запроса:
```json
{
    "phone_number": "71234567890",
    "operator_code": "ABC",
    "tag": "Tag1",
    "timezone": "UTC+3"
}
```
2.Обновление данных получателя:
URL: `/clients/<client_id>/`
Метод: `PUT`
Тело запроса:
```json
{
    "phone_number": "71234567890",
    "operator_code": "XYZ",
    "tag": "Tag2",
    "timezone": "UTC+4"
}
```
3. Добавление новой рассылки:
URL: `/mailings/`
Метод: `POST`
Тело запроса:
```json
{
    "start_time": "2022-01-01T12:00:00",
    "message": "Hello",
    "filter_operator_code": "ABC",
    "filter_tag": "Tag1",
    "end_time": "2022-01-01T18:00:00"
}
```

## Автор: 
- [Андрей Янковский](https://github.com/yonvik)
