from celery import shared_task
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@shared_task()
def send_email(
        full_name: str, email: str,
        pk: int, code: int = None,
        token: str = None, host: str = None
) -> None:
    uid = urlsafe_base64_encode(force_bytes(f"{pk}"))
    context = {
        'name': full_name,
        'code': code,
        'link': f"http://{host}/password-reset/{uid}/{token}"
    }
    html_content = render_to_string('users/verify_email.html', context)
    email = EmailMessage(
        subject='Email Verification',
        body=html_content,
        to=[email]
    )
    email.content_subtype = 'html'
    email.send()
    code and cache.set(pk, code, timeout=60 * 3)
