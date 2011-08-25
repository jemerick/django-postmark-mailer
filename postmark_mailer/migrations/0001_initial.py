# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Message'
        db.create_table('postmark_mailer_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_data', self.gf('django.db.models.fields.TextField')()),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=2)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('postmark_mailer', ['Message'])

        # Adding model 'MessageLog'
        db.create_table('postmark_mailer_messagelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message_data', self.gf('django.db.models.fields.TextField')()),
            ('added', self.gf('django.db.models.fields.DateTimeField')()),
            ('priority', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('attempted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message_id', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('error_code', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('log_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('postmark_mailer', ['MessageLog'])


    def backwards(self, orm):
        
        # Deleting model 'Message'
        db.delete_table('postmark_mailer_message')

        # Deleting model 'MessageLog'
        db.delete_table('postmark_mailer_messagelog')


    models = {
        'postmark_mailer.message': {
            'Meta': {'object_name': 'Message'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_data': ('django.db.models.fields.TextField', [], {}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '2'})
        },
        'postmark_mailer.messagelog': {
            'Meta': {'object_name': 'MessageLog'},
            'added': ('django.db.models.fields.DateTimeField', [], {}),
            'attempted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'message_data': ('django.db.models.fields.TextField', [], {}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'priority': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        }
    }

    complete_apps = ['postmark_mailer']
