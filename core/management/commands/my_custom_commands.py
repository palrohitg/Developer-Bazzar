from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        mail_subject = 'Test mail2'
        message = "text message"
        to_email = "vikasprotobit@gmail.com"

        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        pass
