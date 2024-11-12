from django.contrib import admin

from accounts.models import UserModel, VerificationModel

admin.site.register(UserModel)
admin.site.register(VerificationModel)
