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

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        bookings_to_email = Booking.objects.bookings_to_email()

        # Loop over them and send to guests
        for booking in bookings_to_email:
            try:
                # Send an email to the host(s)
                with transaction.commit_on_success():
                    if not booking.host_emails_sent:
                        host_template = get_template('host_booking_email.txt')
                        subject = 'New booking at {0}'.format(settings.SITE_NAME)
                        self.send_email(settings.HOST_BOOKING_RECIPIENTS, booking, host_template, subject)
                        booking.host_emails_sent = True;
                        booking.save()

                # Send an email to the guest
                with transaction.commit_on_success():
                    if not booking.guest_emails_sent:
                        guest_template = get_template('guest_booking_email.txt')
                        subject = 'Your booking with {0}'.format(settings.SITE_NAME)
                        self.send_email([booking.email], booking, guest_template, subject)

                    booking.guest_emails_sent = True;
                    booking.save()

            except Exception as e:
                logger.error('{0}'.format(e))
                logger.error('Error emailing booking: {0}'.format(booking))

    def send_email(self, recipients, booking, body_template, subject):
        context = Context({'booking': booking, 'settings': settings})
        logger.info('Sending email to: {0} for booking: {1}'.format(recipients, booking))
        mail.send_mail(subject=subject,
                       message=body_template.render(context),
                       from_email=settings.SITE_EMAIL,
                       recipient_list=recipients,
                       fail_silently=False)
