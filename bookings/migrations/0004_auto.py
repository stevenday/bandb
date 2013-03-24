# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Holiday', fields ['start']
        db.create_index('bookings_holiday', ['start'])

        # Adding index on 'Holiday', fields ['end']
        db.create_index('bookings_holiday', ['end'])

        # Adding index on 'Booking', fields ['start']
        db.create_index('bookings_booking', ['start'])

        # Adding index on 'Booking', fields ['end']
        db.create_index('bookings_booking', ['end'])


    def backwards(self, orm):
        # Removing index on 'Booking', fields ['end']
        db.delete_index('bookings_booking', ['end'])

        # Removing index on 'Booking', fields ['start']
        db.delete_index('bookings_booking', ['start'])

        # Removing index on 'Holiday', fields ['end']
        db.delete_index('bookings_holiday', ['end'])

        # Removing index on 'Holiday', fields ['start']
        db.delete_index('bookings_holiday', ['start'])


    models = {
        'bookings.booking': {
            'Meta': {'object_name': 'Booking'},
            'end': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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