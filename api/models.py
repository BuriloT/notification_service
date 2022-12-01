from django.db import models
from django.core.validators import RegexValidator


class Mail(models.Model):
    date_create = models.DateTimeField('время запуска рассылки')
    text = models.TextField('Текст')
    properties = models.CharField('фильтр свойств клиентов', max_length=128)
    date_end = models.DateTimeField('время окончания рассылки')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class Client(models.Model):
    phone_number = models.CharField(
        'номер телефона',
        max_length=11,
        validators=[RegexValidator(
            regex=r'^7[\d]{10}$',
            message=('Неправильный формат. '
                     'Пример: 7XXXXXXXXXX (X - цифра от 0 до 9)')
            )]
        )
    phone_number_code = models.CharField(
        'код мобильного оператора',
        max_length=4
        )
    tag = models.CharField('тег', max_length=128)
    timezone = models.CharField('часовой пояс', max_length=30)

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Message(models.Model):
    date_create = models.DateTimeField('время создания', auto_now_add=True)
    status = models.BooleanField('статус отправки')
    mail = models.ForeignKey(
        Mail,
        verbose_name='рассылка',
        on_delete=models.CASCADE,
        related_name='messages')
    client = models.ForeignKey(
        Client,
        verbose_name='клиент',
        on_delete=models.CASCADE,
        related_name='messages')

    def __str__(self):
        return f'{self.client} - {self.status}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
