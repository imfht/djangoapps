# Generated by Django 2.2.14 on 2020-08-11 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promoted', '0005_auto_20200803_1214'),
        ('discovery', '0006_auto_20200807_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotedAddon',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('promoted.promotedaddon',),
        ),
    ]