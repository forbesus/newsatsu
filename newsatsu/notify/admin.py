from django.contrib import admin

from .models import MailTypeModel, NewsModel, NotificationModel

admin.site.register(NotificationModel)
admin.site.register(NewsModel)
admin.site.register(MailTypeModel)
