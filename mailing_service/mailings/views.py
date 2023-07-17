from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from .models import Client, Mailing, Message
from .serializers import ClientSerializer, MailingSerializer, MessageSerializer


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


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def mailing_statistics(request):
    mailings = Mailing.objects.all()
    total_mailings = mailings.count()
    total_messages = Message.objects.count()
    return Response({
        'total_mailings': total_mailings,
        'total_messages': total_messages,
    })

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
