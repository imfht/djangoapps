# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 16:33
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150530_1541'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'get_latest_by': 'published', 'ordering': ('-published',), 'verbose_name': 'Post', 'verbose_name_plural': 'Posts'},
        ),
        migrations.AlterModelOptions(
            name='revision',
            options={'verbose_name': 'Revision', 'verbose_name_plural': 'Revisions'},
        ),
        migrations.AlterModelOptions(
            name='section',
            options={'verbose_name': 'Section', 'verbose_name_plural': 'Sections'},
        ),
        migrations.AlterField(
            model_name='feedhit',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='feedhit',
            name='request_data',
            field=models.TextField(verbose_name='Request data'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_path',
            field=models.ImageField(upload_to='images/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='image',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='blog.Post', verbose_name='Post'),
        ),
        migrations.AlterField(
            model_name='image',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.CharField(blank=True, max_length=150, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='post',
            name='markup',
            field=models.CharField(choices=[('markdown', 'Markdown')], max_length=25, verbose_name='Markup'),
        ),
        migrations.AlterField(
            model_name='post',
            name='primary_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog.Image', verbose_name='Primary Image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='published',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='post',
            name='secret_key',
            field=models.CharField(blank=True, help_text='allows url for sharing unpublished posts to unauthenticated users', max_length=8, unique=True, verbose_name='Secret key'),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='post',
            name='state',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=1, verbose_name='State'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=90, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tweet_text',
            field=models.CharField(editable=False, max_length=140, verbose_name='Tweet text'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='post',
            name='view_count',
            field=models.IntegerField(default=0, editable=False, verbose_name='View count'),
        ),
        migrations.AlterField(
            model_name='reviewcomment',
            name='addressed',
            field=models.BooleanField(default=False, verbose_name='Addressed'),
        ),
        migrations.AlterField(
            model_name='reviewcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_comments', to='blog.Post', verbose_name='Post'),
        ),
        migrations.AlterField(
            model_name='reviewcomment',
            name='review_text',
            field=models.TextField(verbose_name='Review text'),
        ),
        migrations.AlterField(
            model_name='reviewcomment',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Timestamp'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='content',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to='blog.Post', verbose_name='Post'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='published',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Published'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='teaser',
            field=models.TextField(verbose_name='Teaser'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='title',
            field=models.CharField(max_length=90, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='updated',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Updated'),
        ),
        migrations.AlterField(
            model_name='revision',
            name='view_count',
            field=models.IntegerField(default=0, editable=False, verbose_name='View count'),
        ),
    ]