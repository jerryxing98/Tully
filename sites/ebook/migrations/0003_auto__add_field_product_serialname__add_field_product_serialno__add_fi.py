# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.serialname'
        db.add_column('ebook_product', 'serialname',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'Product.serialno'
        db.add_column('ebook_product', 'serialno',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'Product.publish_on'
        db.add_column('ebook_product', 'publish_on',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.date.today()),
                      keep_default=False)

        # Adding field 'Product.num_page'
        db.add_column('ebook_product', 'num_page',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=8),
                      keep_default=False)

        # Adding field 'Product.publish_type'
        db.add_column('ebook_product', 'publish_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=8),
                      keep_default=False)

        # Adding field 'Product.about'
        db.add_column('ebook_product', 'about',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Product.origin_name'
        db.add_column('ebook_product', 'origin_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'Product.origin_serial'
        db.add_column('ebook_product', 'origin_serial',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=12),
                      keep_default=False)

        # Adding field 'Product.origin_country'
        db.add_column('ebook_product', 'origin_country',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=16),
                      keep_default=False)

        # Adding field 'Product.origin_publish'
        db.add_column('ebook_product', 'origin_publish',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32),
                      keep_default=False)

        # Adding field 'Product.origin_num'
        db.add_column('ebook_product', 'origin_num',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=32),
                      keep_default=False)


        # Changing field 'Product.price'
        db.alter_column('ebook_product', 'price', self.gf('django.db.models.fields.FloatField')())
        

        
        # Adding field 'Article.title'
        db.add_column('ebook_article', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Article.status'
        db.add_column('ebook_article', 'status',
                      self.gf('django.db.models.fields.CharField')(default='draft', max_length=16),
                      keep_default=False)

        # Adding field 'Article.description'
        db.add_column('ebook_article', 'description',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Article.shared'
        db.add_column('ebook_article', 'shared',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Article.content'
        db.add_column('ebook_article', 'content',
                      self.gf('django.db.models.fields.TextField')(default=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.serialname'
        db.delete_column('ebook_product', 'serialname')

        # Deleting field 'Product.serialno'
        db.delete_column('ebook_product', 'serialno')

        # Deleting field 'Product.publish_on'
        db.delete_column('ebook_product', 'publish_on')

        # Deleting field 'Product.num_page'
        db.delete_column('ebook_product', 'num_page')

        # Deleting field 'Product.publish_type'
        db.delete_column('ebook_product', 'publish_type')

        # Deleting field 'Product.about'
        db.delete_column('ebook_product', 'about')

        # Deleting field 'Product.origin_name'
        db.delete_column('ebook_product', 'origin_name')

        # Deleting field 'Product.origin_serial'
        db.delete_column('ebook_product', 'origin_serial')

        # Deleting field 'Product.origin_country'
        db.delete_column('ebook_product', 'origin_country')

        # Deleting field 'Product.origin_publish'
        db.delete_column('ebook_product', 'origin_publish')

        # Deleting field 'Product.origin_num'
        db.delete_column('ebook_product', 'origin_num')


        # Changing field 'Product.price'
        db.alter_column('ebook_product', 'price', self.gf('django.db.models.fields.DecimalField')(max_digits=8, decimal_places=2))
        # Deleting field 'Article.title'
        db.delete_column('ebook_article', 'title')

        # Deleting field 'Article.status'
        db.delete_column('ebook_article', 'status')

        # Deleting field 'Article.description'
        db.delete_column('ebook_article', 'description')

        # Deleting field 'Article.shared'
        db.delete_column('ebook_article', 'shared')

        # Deleting field 'Article.content'
        db.delete_column('ebook_article', 'content')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ebook.article': {
            'Meta': {'object_name': 'Article'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'focus_date': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_favorites': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_replies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rec': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rec_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shared': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'ebook.pdcomment': {
            'Meta': {'object_name': 'PdComment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ebook.Product']"})
        },
        'ebook.product': {
            'Meta': {'object_name': 'Product'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'focus_date': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_favorites': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_page': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'num_replies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'origin_country': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'origin_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'origin_num': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'origin_publish': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'origin_serial': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'publish_on': ('django.db.models.fields.DateTimeField', [], {}),
            'publish_type': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'rec': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rec_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'serialname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'serialno': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'shared': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'draft'", 'max_length': '16'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['ebook']