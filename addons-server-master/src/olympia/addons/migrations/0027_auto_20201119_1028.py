# Generated by Django 2.2.17 on 2020-11-19 10:28

from django.db import migrations, models
import django.db.models.deletion
import django_jsonfield_backport.models


class Migration(migrations.Migration):

    dependencies = [
        ('addons', '0026_addonregionalrestrictions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addonregionalrestrictions',
            options={'verbose_name_plural': 'Addon Regional Restrictions'},
        ),
        migrations.AlterField(
            model_name='addonregionalrestrictions',
            name='addon',
            field=models.OneToOneField(help_text='Add-on id this item will point to', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='regional_restrictions', serialize=False, to='addons.Addon'),
        ),
        migrations.AlterField(
            model_name='addonregionalrestrictions',
            name='excluded_regions',
            field=django_jsonfield_backport.models.JSONField(default=list, help_text='JSON style list of ISO 3166-1 alpha-2 country (region) codes. Codes will be uppercased. E.g. `["CN"]`'),
        ),
    ]