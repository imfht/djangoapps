# Generated by Django 2.2.14 on 2020-08-03 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promoted', '0004_auto_20200731_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotedapproval',
            name='group_id',
            field=models.SmallIntegerField(choices=[(1, 'Recommended'), (2, 'Verified - Tier 1'), (3, 'Verified - Tier 2'), (4, 'Line'), (5, 'Spotlight')], null=True, verbose_name='Group'),
        ),
    ]