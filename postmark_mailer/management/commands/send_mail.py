from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from postmark_mailer.engine import send_batch

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--no-deferred', action='store_false', dest='deferred', default=True,
        help='Do not retry any deferred emails.'),
    )
    
    def handle(self, *args, **options):        
        send_batch()
            