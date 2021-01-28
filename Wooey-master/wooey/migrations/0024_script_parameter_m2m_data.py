# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 14:26
from __future__ import unicode_literals

from django.db import migrations


def update_script_versions(apps, schema_editor):
    ScriptParameter = apps.get_model('wooey', 'ScriptParameter')

    for script_parameter in ScriptParameter.objects.all():
        script_parameter.script_versions.add(script_parameter.script_version)


class Migration(migrations.Migration):

    dependencies = [
        ('wooey', '0023_script_parameter_m2m'),
    ]

    operations = [
        migrations.RunPython(update_script_versions),
    ]