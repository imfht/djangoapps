# Generated by Django 2.2b1 on 2019-03-17 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('openbook_posts', '0022_auto_20190311_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=1120, null=True, verbose_name='text'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='text',
            field=models.CharField(max_length=560, verbose_name='text'),
        ),
    ]