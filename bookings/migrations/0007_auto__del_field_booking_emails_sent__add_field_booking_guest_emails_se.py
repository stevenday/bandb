# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Booking.emails_sent'
        db.delete_column('bookings_booking', 'emails_sent')

        # Adding field 'Booking.guest_emails_sent'
        db.add_column('bookings_booking', 'guest_emails_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Booking.host_emails_sent'
        db.add_column('bookings_booking', 'host_emails_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Booking.emails_sent'
        db.add_column('bookings_booking', 'emails_sent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Deleting field 'Booking.guest_emails_sent'
        db.delete_column('bookings_booking', 'guest_emails_sent')

        # Deleting field 'Booking.host_emails_sent'
        db.delete_column('bookings_booking', 'host_emails_sent')


    models = {
        'bookings.booking': {
            'Meta': {'object_name': 'Booking'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'end': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'guest_emails_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'host_emails_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start': ('django.db.models.fields.DateField', [], {'db_index': 'True'})
        },
        'bookings.holiday': {
            'Meta': {'object_name': 'Holiday'},
            'end': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['bookings']