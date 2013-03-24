# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Booking.name'
        db.add_column('bookings_booking', 'name',
                      self.gf('django.db.models.fields.CharField')(default='Booking', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Booking.name'
        db.delete_column('bookings_booking', 'name')


    models = {
        'bookings.booking': {
            'Meta': {'object_name': 'Booking'},
            'end': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['bookings']