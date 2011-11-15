from django.contrib import admin
from postmark_mailer.models import Message, MessageLog

admin.site.register(Message)
admin.site.register(MessageLog)