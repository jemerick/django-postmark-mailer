VERSION = (0, 1, 0, 'f') # following PEP 386
DEV_N = None


def get_version():
    version = "%s.%s" % (VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "%s.%s" % (version, VERSION[2])
    if VERSION[3] != "f":
        version = "%s%s%s" % (version, VERSION[3], VERSION[4])
        if DEV_N:
            version = "%s.dev%s" % (version, DEV_N)
    return version


__version__ = get_version()

import mimetypes
from django.utils.encoding import force_unicode
from django.conf import settings

try:
    import json                     
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception('Cannot use django-postmark-mailer library without Python 2.6 or greater, or Python 2.4 or 2.5 and the "simplejson" library')


DEFAULT_ATTACHMENT_MIME_TYPE = 'application/octet-stream'

class EmailMessage:
    """A container and sorta replacement for the django.core.mail.EmailMessage"""
    
    def __init__(self, subject=None, body=None, from_email=None, to=None, bcc=None, connection=None, attachments=None, headers=None, cc=None, html_body=None, reply_to=None, tag=None):
        """Initializes a single email message to one or more recipients"""
        self.subject = subject
        self.body = body
        self.html_body = html_body
        self.from_email = from_email
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments
        self.extra_headers = headers
        self.reply_to = reply_to
        self.tag = tag
        
    def attach(self, filename, content, mimetype=None):
        """
        Add an attachement to the email message (does not support email.MIMEBase.MIMEBase instances)
        
        content should be base64 encoded
        
        if mimetype is not provided, one will be guessed based on the filename        
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = DEFAULT_ATTACHMENT_MIME_TYPE
        
        if not attachments:
            attachments = []
        attachments.append({'Name': filename, 'Content': content, 'ContentType': mimetype})
    
    def recipients(self):
        """
        Returns a list of all recipients of the email (includes direct
        addressees as well as Cc and Bcc entries).
        """
        return self.to + self.cc + self.bcc
            
    def send(self, fail_silently=False):
        """
        Inserts the message into the database mail queue
        """
        message_data = {'Subject': self.subject, 'TextBody': self.body, 'From': self.from_email, 'To': ','.join(self.to)}
    
        if self.html_body:
            message_data['HtmlBody'] = self.html_body
    
        if self.cc:
            message_data['Cc'] = ','.join(self.cc)
         
        if self.bcc:
            message_data['Bcc'] = ','.join(self.bcc)
    
        if self.reply_to:
            message_data['ReplyTo'] = self.reply_to
    
        if self.tag:
            message_data['Tag'] = self.tag
        
        if self.extra_headers:
            postmark_headers = []
            for key, value in self.extra_headers.iteritems():
                postmark_headers.append({'Name': key, 'Value': value})
            message_data['Headers'] = postmark_headers
    
        if self.attachments:
            message_data['Attachments'] = attachments
        
        from postmark_mailer.models import Message
        return Message.objects.create(message_data=json.dumps(message_data))

    

# 
def send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    """replacement for django.core.mail.send_mail"""
    
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    message = force_unicode(message)
    
    email_message = EmailMessage(subject=subject, body=message, from_email=from_email, to=recipient_list)
    email_message.send()
    
    return 1


def send_html_mail(subject, message, html_message, from_email, recipient_list, reply_to=None):
    """helper to send HTML e-mails"""
    
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    message = force_unicode(message)
    
    email_message = EmailMessage(subject=subject, body=message, html_body=html_message, from_email=from_email, to=recipient_list)
    email_message.send()

    return 1


def send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    """replacement for django.core.mail.send_mass_mail"""
    num_sent = 0
    for subject, message, sender, recipient in datatuple:
        num_sent += send_mail(subject, message, sender, recipient)
    return num_sent


def mail_admins(subject, message, fail_silently=False, connection=None, html_message=None):    
    """replacement for django.core.mail.mail_admins"""
    return send_html_mail(settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                     message,
                     html_message,
                     settings.SERVER_EMAIL,
                     [a[1] for a in settings.ADMINS])


def mail_managers(subject, message, fail_silently=False, connection=None, html_message=None):
    """replacement for django.core.mail.mail_managers"""    
    return send_html_mail(settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                     message,
                     html_message,
                     settings.SERVER_EMAIL,
                     [a[1] for a in settings.MANAGERS])
