from django.contrib import admin

from .models import MailTypeModel, NotificationModel

admin.site.register(NotificationModel)
admin.site.register(MailTypeModel)
