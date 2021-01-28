# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-23 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humans', '0010_auto_20170526_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyChangeRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prev_fingerprint', models.CharField(blank=True, max_length=50, null=True, verbose_name='Previous Fingerprint')),
                ('to_fingerprint', models.CharField(blank=True, max_length=50, null=True, verbose_name='To Fingerprint')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('agent', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='keychanges', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'KeyChangeRecord',
                'verbose_name_plural': 'KeyChangeRecords',
            },
        ),
    ]