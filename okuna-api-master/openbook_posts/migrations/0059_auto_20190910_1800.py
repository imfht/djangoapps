# Generated by Django 2.2.5 on 2019-09-10 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_posts', '0058_auto_20190902_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postlink',
            name='link',
            field=models.TextField(max_length=5000),
        ),
    ]