from django.utils import timezone
from django.db import models

class Client(models.Model):
    phone_number = models.CharField(max_length=12, unique=True)
    operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)

    def __str__(self):
        return self.phone_number


class Mailing(models.Model):
    start_time = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    filter_operator_code = models.CharField(max_length=10)
    filter_tag = models.CharField(max_length=100)
    end_time = models.DateTimeField()

    def __str__(self):
        return f"Mailing {self.pk}"


class Message(models.Model):
    STATUS_CHOICES = (
        ('sent', 'Sent'),
        ('failed', 'Failed'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    mailing = models.ForeignKey(Mailing, related_name='messages', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, related_name='messages', on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.pk}"
