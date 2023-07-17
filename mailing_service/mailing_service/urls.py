from django.urls import include, path
from rest_framework import routers
from mailings.views import ClientViewSet, MailingViewSet, MessageViewSet, mailing_statistics, mailing_message_statistics

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailings', MailingViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', mailing_statistics, name='mailing_statistics'),
    path('mailings/<int:mailing_id>/statistics/', mailing_message_statistics, name='mailing_message_statistics'),
]
