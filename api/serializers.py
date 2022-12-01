from rest_framework import serializers
from .models import Mail, Client, Message


class ClientSerializer(serializers.ModelSerializer):
    phone_number_code = serializers.CharField(required=False)

    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'phone_number_code', 'tag', 'timezone')

    def create(self, validated_data):
        phone_number = validated_data['phone_number']
        if 'phone_number_code' not in validated_data:
            validated_data['phone_number_code'] = phone_number[1:4]
        client = Client.objects.create(**validated_data)
        return client


class MailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mail
        fields = ('id', 'date_create', 'text', 'properties', 'date_end')

    def create(self, validated_data):
        mail = Mail.objects.create(**validated_data)
        clients = (Client.objects.filter(tag=mail.properties) |
                   Client.objects.filter(phone_number_code=mail.properties))
        for client in clients:
            Message.objects.create(status=False, mail=mail, client=client)
        return mail
