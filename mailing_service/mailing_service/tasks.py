from celery import shared_task
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

@shared_task
def send_message_to_client(message, countdown):
    url = 'https://probe.fbrq.cloud/send_message'
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjA2MjMxMjIsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9hX3lhbmtvdnYifQ.imSengiwB4p3A-gxNqBcsdIj1um7F9C2cSiZcSPMYOM', # Замените YOUR_JWT_TOKEN на ваш токен
        'Content-Type': 'application/json'
    }
    data = {
        'message': message
    }

    try:
        with Session() as session:
            response = session.post(url, headers=headers, json=data)
            response.raise_for_status() 
            return response.json()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None
