from django.conf import settings
from django.core.mail import send_mail

class EmailService():
    def send_simple_mail(self, subject: str, message: str, recipient_list: list):
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f"EmailService.send_simple_mail exc={e}")
