# Generated by Django 2.2.9 on 2020-01-13 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanners', '0018_auto_20200114_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='scannerqueryrule',
            name='state',
            field=models.PositiveSmallIntegerField(choices=[(1, 'New'), (2, 'Running'), (3, 'Aborted'), (4, 'Completed')], default=1),
        ),
        migrations.AlterField(
            model_name='scannerqueryresult',
            name='matched_rules',
            field=models.ManyToManyField(related_name='results', through='scanners.ScannerQueryMatch', to='scanners.ScannerQueryRule'),
        ),
        migrations.AlterField(
            model_name='scannerresult',
            name='matched_rules',
            field=models.ManyToManyField(related_name='results', through='scanners.ScannerMatch', to='scanners.ScannerRule'),
        ),
    ]