from django.contrib import admin
from postmark_mailer.models import Message, MessageLog

class MessageAdmin(admin.ModelAdmin):
    list_filter=('priority',)
    
class MessageLogAdmin(admin.ModelAdmin):
    list_filter=('priority', 'error_code')

admin.site.register(Message, MessageAdmin)
admin.site.register(MessageLog, MessageLogAdmin)
