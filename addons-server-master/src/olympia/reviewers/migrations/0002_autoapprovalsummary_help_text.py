# Generated by Django 2.2.6 on 2019-11-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviewers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autoapprovalsummary',
            name='has_auto_approval_disabled',
            field=models.BooleanField(default=False, help_text='Has auto-approval disabled flag set'),
        ),
        migrations.AlterField(
            model_name='autoapprovalsummary',
            name='is_locked',
            field=models.BooleanField(default=False, help_text='Is locked by a reviewer'),
        ),
        migrations.AlterField(
            model_name='autoapprovalsummary',
            name='is_recommendable',
            field=models.BooleanField(default=False, help_text='Is recommendable'),
        ),
        migrations.AlterField(
            model_name='autoapprovalsummary',
            name='should_be_delayed',
            field=models.BooleanField(default=False, help_text="Delayed because it's the first listed version"),
        ),
    ]