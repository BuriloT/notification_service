from django.contrib import admin
from .models import Mail, Client, Message


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'text', 'date_end', 'properties')
    list_filter = ('date_create', 'date_end', 'properties')
    empty_value_display = '-пусто-'


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'phone_number_code',
                    'tag', 'timezone')
    list_filter = ('phone_number_code', 'tag', 'timezone')
    empty_value_display = '-пусто-'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'status', 'client', 'mail')
    list_filter = ('status', 'date_create', 'client', 'mail')
    empty_value_display = '-пусто-'
