from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from celery import shared_task

@shared_task
def send_html_template_email(to, subject, template_name, context):
    try:
        template = get_template(template_name)
        content = template.render(context=context)

        return send_mail(
            subject=subject,
            message="",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=to,
            html_message=content
        )
    except Exception as e:
        raise e