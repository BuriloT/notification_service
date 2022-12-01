import os
import requests
from datetime import datetime as dt
from dotenv import load_dotenv
from django.db import transaction
from django.db.models import Q
from notification_service.settings import dotenv_file
from notification_service.celery import app
from .models import Mail

load_dotenv(dotenv_file)


def send_request(message_id, phone, text):
    url = f'https://probe.fbrq.cloud/v1/send/{message_id}'
    token = os.getenv('TOKEN')
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }
    data = {
        'id': message_id,
        'phone': phone,
        'text': text
    }
    return requests.post(url=url, json=data, headers=headers).status_code


@app.task()
def send_mail():
    with transaction.atomic():
        now = dt.now()

        criterion1 = Q(date_create__lt=now)
        criterion2 = Q(date_end__gt=now)
        mails = Mail.objects.filter(criterion1 & criterion2)
        for mail in mails:
            for message in mail.messages.filter(status=False):
                req_status_code = send_request(
                    message.id,
                    message.client.phone_number,
                    mail.text
                )
                if req_status_code == 200:
                    message.status = True
                    message.save()
                else:
                    return f'Произошла ошибка {req_status_code} на стороннем API'
