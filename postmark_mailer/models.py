from django.db import models

try:
    import json                     
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception('Cannot use python-postmark library without Python 2.6 or greater, or Python 2.4 or 2.5 and the "simplejson" library')


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
        self.priority = PRIORITY_DEFERRED
        self.save()

    def __unicode__(self):
        return u"Message"

def make_message(subject, message, from_email, to_list, message_html=None, cc_list=None, bcc_list=None, priority=2, reply_to=None, headers=None, tag=None, attachements=None):
    message_data = {'Subject': subject, 'TextBody': message, 'From': from_email, 'To': ','.join(to_list)}
    
    if message_html:
        message_data['HtmlBody'] = message_html
    
    if cc_list:
        message_data['Cc'] = ','.join(cc_list)
         
    if bcc_list:
        message_data['Bcc'] = ','.join(bcc_list)
    
    if reply_to:
        message_data['ReplyTo'] = reply_to
    
    if tag:
        message_data['Tag'] = tag
        
    if headers:
        postmark_headers = []
        for key, value in headers.iteritems():
            postmark_headers.append({'Name': key, 'Value': value})
        message_data['Headers'] = postmark_headers
    
    if attachements:
        message_data['Attachments'] = attachements
        
    return Message.objects.create(message_data=json.dumps(message_data), priority=priority)


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
