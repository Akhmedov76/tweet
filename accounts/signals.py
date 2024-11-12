import threading

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from Config.settings import EMAIL_HOST_USER
from accounts.models import UserModel


def send_verification_email(email):
    send_mail(
        subject="Email Verification",
        message="Please verify your email address by clicking the link below:\n\n"
                f"http://localhost:8000/verify/{email}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )


@receiver(post_save, sender=UserModel)
def send_verification_email_after_signup(sender, instance=None, created=False, **kwargs):
    if created:
        email_thread = threading.Thread(target=send_verification_email, args=(instance.email))
        email_thread.start()
