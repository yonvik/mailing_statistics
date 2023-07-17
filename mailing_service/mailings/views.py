from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from celery.result import AsyncResult
from .models import Client, Mailing, Message
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer
from mailing_service.tasks import send_message_to_client


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class MailingViewSet(viewsets.ModelViewSet):
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.query_params.get('tag')
        operator_code = self.request.query_params.get('operator_code')
        if tag:
            queryset = queryset.filter(filter_tag=tag)
        if operator_code:
            queryset = queryset.filter(filter_operator_code=operator_code)
        return queryset

    def create(self, request, *args, **kwargs):
        message = request.POST.get('message')

        if not message:
            return JsonResponse({'error': 'Message is required.'}, status=400)

        send_message_to_client.delay(message)

        return JsonResponse({'message': 'Message sent successfully.'})


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        mailing_id = self.request.query_params.get('mailing_id')
        client_id = self.request.query_params.get('client_id')
        if mailing_id:
            queryset = queryset.filter(mailing_id=mailing_id)
        if client_id:
            queryset = queryset.filter(client_id=client_id)
        return queryset


def mailing_statistics(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            task = send_message_to_client.delay(message)
            return JsonResponse({
                'task_id': task.id,
                'task_status': task.status,
            })
        else:
            return JsonResponse({'error': 'Message is required'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def mailing_message_statistics(request, mailing_id):
    try:
        mailing = Mailing.objects.get(id=mailing_id)
    except Mailing.DoesNotExist:
        return Response({'error': 'Mailing not found'}, status=404)
    total_messages = mailing.message_set.count()

    sent_messages = mailing.message_set.filter(status='sent').count()

    pending_messages = mailing.message_set.filter(status='pending').count()

    return Response({
        'mailing_id': mailing.id,
        'total_messages': total_messages,
        'sent_messages': sent_messages,
        'pending_messages': pending_messages,
    })
