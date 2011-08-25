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


from django.utils.encoding import force_unicode
from django.conf import settings
from postmark_mailer import Message

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
    

# replacement for django.core.mail.send_mail
def send_mail(subject, message, from_email, recipient_list, priority=2, fail_silently=False, auth_user=None, auth_password=None):
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    message = force_unicode(message)
    
    make_message(subject=subject, message=message, from_email=from_email, to_list=recipient_list, priority=priority)
    return 1


def send_html_mail(subject, message, message_html, from_email, recipient_list, priority=2, reply_to=None):
    """
    Function to queue HTML e-mails
    """
    
    # need to do this in case subject used lazy version of ugettext
    subject = force_unicode(subject)
    message = force_unicode(message)
    
    make_message(subject=subject, message=message, message_html=message_html, from_email=from_email, to_list=recipient_list, priority=priority. reply_to=reply_to)

    return 1


def send_mass_mail(datatuple, fail_silently=False, auth_user=None, auth_password=None, connection=None):
    num_sent = 0
    for subject, message, sender, recipient in datatuple:
        num_sent += send_mail(subject, message, sender, recipient)
    return num_sent


def mail_admins(subject, message, fail_silently=False, connection=None, priority=2):    
    return send_mail(settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                     message,
                     settings.SERVER_EMAIL,
                     [a[1] for a in settings.ADMINS])


def mail_managers(subject, message, fail_silently=False, connection=None, priority=2):    
    return send_mail(settings.EMAIL_SUBJECT_PREFIX + force_unicode(subject),
                     message,
                     settings.SERVER_EMAIL,
                     [a[1] for a in settings.MANAGERS])
