# Generated by Django 2.2.12 on 2020-06-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('addons', '0008_auto_20200604_0928')]

    operations = [
        migrations.AlterField(
            model_name='addon',
            name='public_stats',
            field=models.NullBooleanField(
                db_column='publicstats', default=False
            ),
        )
    ]