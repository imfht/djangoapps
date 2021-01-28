# Generated by Django 2.2.14 on 2020-07-09 10:37

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import olympia.amo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('versions', '0008_auto_20200625_1114'),
        ('addons', '0014_remove_addon_view_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromotedApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('group_id', models.SmallIntegerField(choices=[(1, 'Recommended'), (2, 'Verified - Tier 1'), (3, 'Verified - Tier 2'), (4, 'Line'), (5, 'Spotlight'), (6, 'Strategic')], null=True)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promoted_approvals', to='versions.Version')),
            ],
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PromotedAddon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('group_id', models.SmallIntegerField(choices=[(0, 'Not Promoted'), (1, 'Recommended'), (2, 'Verified - Tier 1'), (3, 'Verified - Tier 2'), (4, 'Line'), (5, 'Spotlight'), (6, 'Strategic')], default=0)),
                ('addon', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='addons.Addon')),
            ],
            options={
                'get_latest_by': 'created',
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=(olympia.amo.models.SearchMixin, olympia.amo.models.SaveUpdateMixin, models.Model),
        ),
        migrations.AddConstraint(
            model_name='promotedapproval',
            constraint=models.UniqueConstraint(fields=('group_id', 'version'), name='unique_promoted_version'),
        ),
    ]