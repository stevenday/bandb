import logging
from datetime import datetime

from django.core import mail
from django.core.management.base import NoArgsCommand
from django.db import transaction
from django.template.loader import get_template
from django.conf import settings
from django.template import Context

from ...models import Booking

logger = logging.getLogger(__name__)

@transaction.commit_manually
class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        bookings_to_email = Booking.objects.bookings_to_email()

        # Loop over them and send to guests
        for booking in bookings_to_email:
            try:
                # FIXME: theoretically, this could send to the host, and then fail
                # on sending to the guest, hence not setting booking.emails_sent
                # and causing email(s) to be sent again.
                # They're this way round for a reason - the host doesn't care so much!

                # Send an email to the host(s)
                host_template = get_template('host_booking_email.txt')
                subject = 'New booking at {0}'.format(settings.SITE_NAME)
                self.send_email(settings.HOST_BOOKING_RECIPIENTS, booking, host_template, subject)

                # Send an email to the guest
                guest_template = get_template('guest_booking_email.txt')
                subject = 'Your booking with {0}'.format(settings.SITE_NAME)
                self.send_email([booking.email], booking, guest_template, subject)

                # Record that we sent it
                booking.emails_sent = True;
                booking.save()
                transaction.commit()
            except Exception as e:
                logger.error('{0}'.format(e))
                logger.error('Error emailing booking: {0}'.format(booking))
                transaction.rollback()

    def send_email(self, recipients, booking, body_template, subject):
        context = Context({'booking': booking})
        logger.info('Sending email to: {0} for booking: {1}'.format(recipients, booking))
        mail.send_mail(subject=subject,
                       message=body_template.render(context),
                       from_email=settings.SITE_EMAIL,
                       recipient_list=recipients,
                       fail_silently=False)
