# Generated by Django 2.2.5 on 2019-09-12 13:36

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import olympia.amo.fields
import olympia.amo.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('addons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', olympia.amo.fields.PositiveAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('date_posted', models.DateField(default=datetime.datetime.now)),
                ('permalink', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'blogposts',
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RssKey',
            fields=[
                ('id', olympia.amo.fields.PositiveAutoField(primary_key=True, serialize=False)),
                ('key', models.UUIDField(db_column='rsskey', default=uuid.uuid4, null=True, unique=True)),
                ('created', models.DateField(default=datetime.datetime.now)),
                ('addon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='addons.Addon', unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'db_table': 'hubrsskeys',
            },
        ),
    ]