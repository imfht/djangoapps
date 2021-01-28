# Generated by Django 2.2.6 on 2020-01-07 16:50

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields.json
import olympia.amo.models


class Migration(migrations.Migration):

    dependencies = [
        ('versions', '0003_drop_version_int_column'),
        ('scanners', '0016_scannerrule_definition'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScannerQueryMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': 'created',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.AlterModelOptions(
            name='scannerresult',
            options={'base_manager_name': 'objects', 'get_latest_by': 'created'},
        ),
        migrations.AlterModelOptions(
            name='scannerrule',
            options={'base_manager_name': 'objects', 'get_latest_by': 'created'},
        ),
        migrations.AlterField(
            model_name='scannerresult',
            name='upload',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='scannerresults', to='files.FileUpload'),
        ),
        migrations.AlterField(
            model_name='scannerresult',
            name='version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scannerresults', to='versions.Version'),
        ),
        migrations.CreateModel(
            name='ScannerQueryRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='This is the exact name of the rule used by a scanner.', max_length=200)),
                ('scanner', models.PositiveSmallIntegerField(choices=[(1, 'customs'), (2, 'wat'), (3, 'yara')])),
                ('action', models.PositiveSmallIntegerField(choices=[(1, 'No action'), (20, 'Flag for human review'), (100, 'Delay auto-approval'), (200, 'Delay auto-approval indefinitely')], default=1)),
                ('is_active', models.BooleanField(default=True)),
                ('definition', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'scanners_query_rules',
                'get_latest_by': 'created',
                'abstract': False,
                'base_manager_name': 'objects',
                'unique_together': {('name', 'scanner')},
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ScannerQueryResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('results', django_extensions.db.fields.json.JSONField(default=[])),
                ('scanner', models.PositiveSmallIntegerField(choices=[(1, 'customs'), (2, 'wat'), (3, 'yara')])),
                ('has_matches', models.NullBooleanField()),
                ('state', models.PositiveSmallIntegerField(blank=True, choices=[(None, 'Unknown'), (1, 'True positive'), (2, 'False positive')], default=None, null=True)),
                ('matched_rules', models.ManyToManyField(through='scanners.ScannerQueryMatch', to='scanners.ScannerQueryRule')),
                ('version', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scannerqueryresults', to='versions.Version')),
            ],
            options={
                'db_table': 'scanners_query_results',
                'get_latest_by': 'created',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.AddField(
            model_name='scannerquerymatch',
            name='result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanners.ScannerQueryResult'),
        ),
        migrations.AddField(
            model_name='scannerquerymatch',
            name='rule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanners.ScannerQueryRule'),
        ),
        migrations.AddIndex(
            model_name='scannerqueryresult',
            index=models.Index(fields=['has_matches'], name='scanners_qu_has_mat_a6766b_idx'),
        ),
        migrations.AddIndex(
            model_name='scannerqueryresult',
            index=models.Index(fields=['state'], name='scanners_qu_state_32d49e_idx'),
        ),
    ]