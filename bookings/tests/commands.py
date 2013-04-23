import logging
from mock import patch

from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.template import Context
from django.template.loader import get_template
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.translation import activate

from .helpers import create_test_booking
from ..models import Booking

@override_settings(HOST_BOOKING_RECIPIENTS=['host@example.com'])
class SendBookingsEmailsCommandTests(TestCase):

    def setUp(self):
        # Set the locale to en-gb, so we use our date formats
        activate('en-gb')

    def _call_command(self):
        args = []
        opts = {}
        call_command('send_bookings_emails', *args, **opts)

    def test_happy_path(self):
        # Create a booking which should be emailed
        booking = create_test_booking({'paid':True})

        # Run the command
        self._call_command()

        self.assertEqual(len(mail.outbox), 2)

        # First email should be the one to the host
        first_mail = mail.outbox[0]
        self.assertEqual(first_mail.subject, 'New booking at {0}'.format(settings.SITE_NAME))
        self.assertEqual(first_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(first_mail.to, settings.HOST_BOOKING_RECIPIENTS)
        template = get_template('host_booking_email.txt')
        context = Context({'booking': booking})
        expected_body = template.render(context)
        self.assertEqual(first_mail.body, expected_body)

        # Last email should be the one to the guest
        second_mail = mail.outbox[1]
        self.assertEqual(second_mail.subject, 'Your booking with {0}'.format(settings.SITE_NAME))
        self.assertEqual(second_mail.from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(second_mail.to, [booking.email])
        template = get_template('guest_booking_email.txt')
        context = Context({'booking': booking})
        expected_body = template.render(context)
        self.assertEqual(second_mail.body, expected_body)

    def test_ignores_unconfirmed_bookings(self):
        # Create a booking which should not be emailed because it's unconfirmed
        booking = create_test_booking()

        # Run the command
        self._call_command()

        self.assertEqual(len(mail.outbox), 0)

    def test_ignores_bookings_already_sent(self):
        # Create a booking which should not be emailed because its'
        # already been sent
        booking = create_test_booking({'paid': True, 'emails_sent': True})

        # Run the command
        self._call_command()

        self.assertEqual(len(mail.outbox), 0)

    def test_handles_errors_in_emailing(self):
        # Create a booking which should be emailed
        booking = create_test_booking({'paid':True})

        # Quiet logging for this test
        logging.disable(logging.CRITICAL)

        # Make send_mail throw an exception on the second call
        old_send_mail = mail.send_mail
        with patch.object(mail, 'send_mail') as mock_send_mail:
            # Set side effects so that the second mail fails
            mock_send_mail.side_effect = [1, Exception('A fake error in sending mail')]
            self._call_command()

            # Check that the booking is still marked as not mailed
            booking = Booking.objects.get(pk=booking.id)
            self.assertFalse(booking.emails_sent)

        # Re-enable logging
        logging.disable(logging.NOTSET)

