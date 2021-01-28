# Generated by Django 2.2.6 on 2019-10-23 09:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import olympia.amo.models


class Migration(migrations.Migration):

    dependencies = [
        ('scanners', '0008_auto_20191021_1718'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScannerMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanners.ScannerResult')),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanners.ScannerRule')),
            ],
            options={
                'get_latest_by': 'created',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.AddField(
            model_name='scannerresult',
            name='matched_rules',
            field=models.ManyToManyField(through='scanners.ScannerMatch', to='scanners.ScannerRule'),
        ),
    ]