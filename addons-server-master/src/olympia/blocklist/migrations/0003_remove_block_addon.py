# Generated by Django 2.2.6 on 2019-11-07 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocklist', '0002_auto_20191107_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='block',
            name='addon',
        ),
        migrations.AlterField(
            model_name='block',
            name='guid',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]