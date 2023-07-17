from rest_framework import serializers
from .models import Client, Mailing, Message


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'phone_number', 'operator_code', 'tag', 'timezone')


class MailingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailing
        fields = ('id', 'start_time', 'message', 'filter_operator_code', 'filter_tag', 'end_time')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'created_at', 'status', 'mailing', 'client')
