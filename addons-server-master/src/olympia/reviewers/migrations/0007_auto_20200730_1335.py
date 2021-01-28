# Generated by Django 2.2.14 on 2020-07-30 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewers', '0006_auto_20200609_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='autoapprovalsummary',
            name='is_promoted_prereview',
            field=models.BooleanField(default=None, help_text='Is in a promoted addon group that requires pre-review', null=True),
        ),
        migrations.AlterField(
            model_name='autoapprovalsummary',
            name='is_recommendable',
            field=models.BooleanField(default=False, help_text='Is in the recommended promoted addon group', null=True),
        ),
    ]