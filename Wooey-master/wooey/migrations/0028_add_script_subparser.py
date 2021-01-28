# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-04-25 09:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wooey.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('wooey', '0027_parameter_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScriptParser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, default='')),
                ('script_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wooey.ScriptVersion')),
            ],
            bases=(wooey.models.mixins.WooeyPy2Mixin, models.Model),
        ),
        migrations.AddField(
            model_name='scriptparameter',
            name='parser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wooey.ScriptParser'),
            preserve_default=False,
        ),
    ]