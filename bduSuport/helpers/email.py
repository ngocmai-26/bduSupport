from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.template.loader import get_template
from celery import shared_task
import logging

@shared_task
def send_html_template_email(to, subject, template_name, context):
    try:
        logging.info("shared_task send_html_template_email to=%s, subject=%s, template_name=%s, context=%s", to, subject, template_name, context)
        logging.info("shared_task send_html_template_email user=%s, password=%s", settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        template = get_template(template_name)
        content = template.render(context=context)

        return send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to,
            html_message=content,
            connection=get_connection()
        )
    except Exception as e:
        logging.exception("shared_task send_html_template_email exc=%s, to=%s, subject=%s, template_name=%s, context=%s", e, to, subject, template_name, context)
        raise e