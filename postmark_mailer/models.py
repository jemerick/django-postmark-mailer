from django.db import models

class Message(models.Model):
    """An email message"""
    
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3
    PRIORITY_DEFERRED = 4
    
    PRIORITES = (
        (PRIORITY_HIGH, "high"),
        (PRIORITY_MEDIUM, "medium"),
        (PRIORITY_LOW, "low"),
        (PRIORITY_DEFERRED, "deferred"),
    )
    
    message_data = models.TextField()    
    priority = models.PositiveSmallIntegerField(default=2)
    added = models.DateTimeField(auto_now_add=True)
    
    def defer(self):
        self.priority = self.PRIORITY_DEFERRED
        self.save()

    def __unicode__(self):
        return u"Message"


class MessageLog(models.Model):
    """A log of sent emails"""
    
    message_data = models.TextField()
    added = models.DateTimeField()
    priority = models.PositiveSmallIntegerField()
    
    attempted = models.DateTimeField(auto_now_add=True)
    message_id = models.CharField(blank=True, null=True, max_length=80)
    error_code = models.IntegerField(default=0)
    log_message = models.TextField(blank=True, null=True)
    

    def __unicode__(self):
        return u"MessageLog"
