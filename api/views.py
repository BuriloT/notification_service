from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import Mail, Client, Message
from .serializers import ClientSerializer, MailSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailViewSet(viewsets.ModelViewSet):
    queryset = Mail.objects.all()
    serializer_class = MailSerializer

    @action(detail=True, methods=['GET'])
    def detail_statistic(self, request, pk):
        mail = self.get_object()
        messages = Message.objects.filter(mail=mail)
        status_true_count = messages.filter(status=True).count()
        status_false_count = messages.filter(status=False).count()
        data = {
            'date_create': mail.date_create,
            'text': mail.text,
            'properties': mail.properties,
            'date_end': mail.date_end,
            'status_true_count': status_true_count,
            'status_false_count': status_false_count,
            'messages_count': messages.count()
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def common_statistic(self, request):
        result = []
        for mail in self.queryset:
            messages = Message.objects.filter(mail=mail)
            status_true_count = messages.filter(status=True).count()
            status_false_count = messages.filter(status=False).count()
            result.append({
                'mail_id': mail.id,
                'mail_date_create': mail.date_create,
                'mail_date_end': mail.date_end,
                'status_true_count': status_true_count,
                'status_false_count': status_false_count,
                'messages_count': messages.count(),
            })
        return Response(data=result, status=status.HTTP_200_OK)
