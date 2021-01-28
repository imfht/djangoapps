# Generated by Django 2.2.14 on 2020-10-02 10:06

from django.db import migrations


def clear_user_restriction_history(apps, schema_editor):
    fields = {'last_login_ip': '', 'ip_address': ''}
    UserRestrictionHistory = apps.get_model('users', 'UserRestrictionHistory')
    qs = UserRestrictionHistory.objects.filter(
        user__last_login_ip='', user__deleted=True).exclude(**fields)
    qs.update(**fields)


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200624_0225'),
    ]

    operations = [
        migrations.RunPython(clear_user_restriction_history)
    ]