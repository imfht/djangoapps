# Generated by Django 2.2.5 on 2019-09-12 15:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields.json
import olympia.amo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('versions', '0001_initial'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YaraResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('matches', django_extensions.db.fields.json.JSONField(default=[])),
                ('upload', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='yara_results', to='files.FileUpload')),
                ('version', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='yara_results', to='versions.Version')),
            ],
            options={
                'db_table': 'yara_results',
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
    ]