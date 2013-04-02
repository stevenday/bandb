# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Booking.email'
        db.add_column('bookings_booking', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='not_set@example.com', max_length=255),
                      keep_default=False)

        # Adding field 'Booking.notes'
        db.add_column('bookings_booking', 'notes',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Booking.paid'
        db.add_column('bookings_booking', 'paid',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Booking.email'
        db.delete_column('bookings_booking', 'email')

        # Deleting field 'Booking.notes'
        db.delete_column('bookings_booking', 'notes')

        # Deleting field 'Booking.paid'
        db.delete_column('bookings_booking', 'paid')


    models = {
        'bookings.booking': {
            'Meta': {'object_name': 'Booking'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'end': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
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