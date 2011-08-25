from django.conf import settings
from postmark_mailer.models import Message, MessageLog
import sys
import requests

try:
    import json                     
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception('Cannot use python-postmark library without Python 2.6 or greater, or Python 2.4 or 2.5 and the "simplejson" library')

POSTMARK_API_BATCH_URL = 'https://api.postmarkapp.com/email/batch'
POSTMARK_API_KEY = getattr(settings, "POSTMARK_API_KEY", "POSTMARK_API_TEST")

def send_batch(retry_deferred=True, test=False):
    
    api_key = test and 'POSTMARK_API_TEST' or POSTMARK_API_KEY
    
    batch_size = getattr(settings, "POSTMARK_BATCH_SIZE", 500)
    if batch_size > 500:
        batch_size = 500
    
    if retry_deferred:
        priority_level = Message.PRIORITY_DEFERRED
    else:
        priority_level = Message.PRIORITY_LOW
        
    messages = Message.objects.filter(priority__lte=priority_level).order_by('priority')[:batch_size]
    
    batch_data = '[%s]' % ','.join([message.message_data for message in messages])
    
    postmark_request = requests.post(POSTMARK_API_BATCH_URL, batch_data, headers={'X-Postmark-Server-Token': api_key, 'Content-Type': 'application/json', 'Accept': 'application/json'})
    
    if postmark_request.status_code == 200:
        batch_logs = json.loads(postmark_request.content)
        
        message_logs = zip(messages, batch_logs)
        
        for message, response in message_logs:
            error_code = response.get('ErrorCode')
            log_message = response.get('Message')
            message_id = response.get('MessageID')
            
            MessageLog.objects.create(message_data=message.message_data, added=message.added, priority=message.priority, error_code=error_code, log_message=log_message, message_id=message_id)

            if error_code == 0:
                message.delete()
            else:
                message.defer()
                
    elif postmark_request.status_code == 401:
        raise Exception('401 - Missing or incorrect API key.')
        
    elif postmark_request.status_code == 422:
        error = json.loads(r.content)        
        raise Exception('422 - %s:%s' % (error.get('ErrorCode'), error.get('Message')))
        
    elif postmark_request.status_code == 500:
        raise Exception('500 - Postmark Server Error')
                