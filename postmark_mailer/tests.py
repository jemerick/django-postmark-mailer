from postmark_mailer.models import Message, MessageLog, make_message
from postmark_mailer.engine import send_batch
from postmark_mailer import send_mail, send_html_mail


from django.test import TestCase

try:
    import json                     
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception('Cannot use python-postmark library without Python 2.6 or greater, or Python 2.4 or 2.5 and the "simplejson" library')


class MakeMessageTest(TestCase):
    
    def test_make_message(self):
        message = make_message('subject', 'text message', 'jason@mobelux.com', ['jemerick@gmail.com'], message_html='html message', cc_list=['garrett@mobelux.com', 'jeff@mobelux.com'], bcc_list=None, priority=1, reply_to='carousel@mobelux.com', headers={'X-Mailer': 'django-postmark-mailer'}, tag="tag")
        
        self.assertEqual(message.priority, 1)
        
        email = json.loads(message.message_data)
        
        self.assertEqual(email.get('Subject'), 'subject')
        self.assertEqual(email.get('TextBody'), 'text message')
        self.assertEqual(email.get('From'), 'jason@mobelux.com')
        self.assertEqual(email.get('To'), 'jemerick@gmail.com')
        self.assertEqual(email.get('HtmlBody'), 'html message')
        self.assertEqual(email.get('Cc'), 'garrett@mobelux.com,jeff@mobelux.com')
        self.assertEqual(email.get('Bcc'), None)
        self.assertEqual(email.get('ReplyTo'), 'carousel@mobelux.com')
        self.assertEqual(email.get('Tag'), 'tag')
        
        headers = email.get('Headers')
        
        self.assertEqual(len(headers), 1)
        self.assertEqual(headers[0].get('Name'), 'X-Mailer')
        self.assertEqual(headers[0].get('Value'), 'django-postmark-mailer')
        
        
    def test_send_mail(self):
        send_mail('subject', 'message', 'jason@mobelux.com', ['jemerick@gmail.com', 'jason@emerick.org'])
        
        message = next(iter(Message.objects.all()), None)
        self.assertEqual(message.priority, 2)
        email = json.loads(message.message_data)
        
        self.assertEqual(email.get('Subject'), 'subject')
        self.assertEqual(email.get('TextBody'), 'message')
        self.assertEqual(email.get('From'), 'jason@mobelux.com')
        self.assertEqual(email.get('To'), 'jemerick@gmail.com,jason@emerick.org')
        self.assertEqual(email.get('HtmlBody'), None)
        self.assertEqual(email.get('Cc'), None)
        self.assertEqual(email.get('Bcc'), None)
        self.assertEqual(email.get('ReplyTo'), None)
        self.assertEqual(email.get('Tag'), None)
        self.assertEqual(email.get('Headers'), None)
    
    def test_send_html_mail(self):
        send_html_mail('subject', 'message', 'html message', 'jason@mobelux.com', ['jemerick@gmail.com', 'jason@emerick.org'])
        
        message = next(iter(Message.objects.all()), None)
        self.assertEqual(message.priority, 2)
        email = json.loads(message.message_data)
        
        self.assertEqual(email.get('Subject'), 'subject')
        self.assertEqual(email.get('TextBody'), 'message')
        self.assertEqual(email.get('From'), 'jason@mobelux.com')
        self.assertEqual(email.get('To'), 'jemerick@gmail.com,jason@emerick.org')
        self.assertEqual(email.get('HtmlBody'), 'html message')
        self.assertEqual(email.get('Cc'), None)
        self.assertEqual(email.get('Bcc'), None)
        self.assertEqual(email.get('ReplyTo'), None)
        self.assertEqual(email.get('Tag'), None)
        self.assertEqual(email.get('Headers'), None)

class SendBatchTest(TestCase):
    
    MESSAGE_1 = """{
        "From": "Talk <asdf@asdf.com>",
        "To": "jemerick@gmail.com,jason@mobelux.com",
        "Subject": "Test",
        "Tag": "test",
        "HtmlBody": "<b>Hello</b>",
        "TextBody": "Hello",
        "ReplyTo": "carousel@mobelux.com"
    }"""
    
    MESSAGE_2 = """{
        "From": "Talk <carousel@mobelux.com>",
        "To": "jason@mobelux.com",
        "Subject": "Test",
        "Tag": "test",
        "HtmlBody": "<b>Hello</b>",
        "TextBody": "Hello",
        "ReplyTo": "carousel@mobelux.com"
    }"""
    
    def setUp(self):
        
        Message.objects.create(message_data=self.MESSAGE_1)
        Message.objects.create(message_data=self.MESSAGE_2)
        
    def test_send_batch_of_two(self):
        
        send_batch(test=True)
        
        self.assertEqual(Message.objects.all().count(), 0)
        self.assertEqual(MessageLog.objects.all().count(), 2)
        
        message_logs = MessageLog.objects.all()
        
        for message_log in message_logs:
            self.assertEqual(message_log.error_code, 0)
        
    



