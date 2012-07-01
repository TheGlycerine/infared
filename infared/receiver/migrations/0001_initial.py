# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'IRCode'
        db.create_table('receiver_ircode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('receiver', ['IRCode'])

        # Adding model 'IRCodeInfo'
        db.create_table('receiver_ircodeinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bit_count', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('encoding', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('gap', self.gf('django.db.models.fields.IntegerField')(max_length=10, null=True, blank=True)),
            ('trail', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('repeat', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024, null=True, blank=True)),
            ('header', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024, null=True, blank=True)),
            ('zero', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024, null=True, blank=True)),
            ('one', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=1024, null=True, blank=True)),
            ('min_repeat', self.gf('django.db.models.fields.IntegerField')(max_length=3, null=True, blank=True)),
            ('carrier_frequency', self.gf('django.db.models.fields.IntegerField')(max_length=30, null=True, blank=True)),
            ('duty_cycle', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal('receiver', ['IRCodeInfo'])


    def backwards(self, orm):
        
        # Deleting model 'IRCode'
        db.delete_table('receiver_ircode')

        # Deleting model 'IRCodeInfo'
        db.delete_table('receiver_ircodeinfo')


    models = {
        'receiver.ircode': {
            'Meta': {'object_name': 'IRCode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'receiver.ircodeinfo': {
            'Meta': {'object_name': 'IRCodeInfo'},
            'bit_count': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'carrier_frequency': ('django.db.models.fields.IntegerField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'duty_cycle': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'encoding': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'gap': ('django.db.models.fields.IntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'header': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'min_repeat': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'one': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'repeat': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'trail': ('django.db.models.fields.IntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'zero': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['receiver']
