import random

from accounts.models import VerificationModel


def get_random_verification_code(email):
    code = random.randint(1000, 9999)
    while VerificationModel.objects.filter(user__email=email, code=code).exists():
        code = random.randint(1000, 9999)
    return code
