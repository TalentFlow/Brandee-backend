from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings 

import threading

from .serializers import UserSerializer
import datetime
from django.utils import timezone

expire=settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


def custom_jwt_response_handler(token, user=None, request=None):
    return {
        'token' : token,
        'user' : UserSerializer(user, context={'request' : request}).data,
        'expire':timezone.now()+expire-datetime.timedelta(seconds=200)
    }

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Util:
    @staticmethod
    def send_email(data):
        subject, from_email, to = data['email_subject'], settings.EMAIL_HOST_USER, data['to_email']
        text_content = 'Thanks .'
        html_content = '<h1>Hi,</h1>'+ '<h1>'+ data['first_name']+' ' + data['last_name']+ '!' + '</h1>' +'<br/><h3>Thanks for <strong>Registering</strong> to our Website.</h3><br/><h3>Hope to see you again and agin.</h3>'
        msg = EmailMultiAlternatives(subject, text_content,  from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        EmailThread(msg).start()

class Utils:
    @staticmethod
    def send_email(data):
        subject, from_email, to = data['email_subject'], settings.EMAIL_HOST_USER, data['to_email']
        text_content = 'Reset Password.'
        html_content = '<h1>Hi,</h1>'+ '<h1>'+ data['first_name']+' ' + data['last_name']+ '!' + '</h1>' +'<br/><h3>This is your <strong>Reset Password</strong> Link.</h3><br/><h3>Click the link to change your password.</h3><br/>'+ data['email_body']
        msg = EmailMultiAlternatives(subject, text_content,  from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        print(msg)
        EmailThread(msg).start()
