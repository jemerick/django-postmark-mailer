from postmark_mailer.models import Message, MessageLog
from postmark_mailer.engine import send_batch

from django.test import TestCase

class SendBatchTest(TestCase):
    
    MESSAGE_1 = """{
        "From": "Talk <asdf@asdf.com>",
        "To": "jemerick@gmail.com, jason@mobelux.com",
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
        
    



