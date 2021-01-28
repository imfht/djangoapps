# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-25 20:24

from django.db import migrations

from sentry.utils.query import RangeQuerySetWrapperWithProgressBar


def backfill_rule_level_fields(apps, schema_editor):
    AlertRule = apps.get_model("sentry", "AlertRule")
    for alert_rule in RangeQuerySetWrapperWithProgressBar(AlertRule.objects_with_snapshots.all()):
        triggers = list(alert_rule.alertruletrigger_set.all())
        # Determine the resolve_threshold and threshold_type from the rule's triggers
        if triggers:
            # Threshold types are the same for all triggers on a rule, so just grab one
            threshold_type = triggers[0].threshold_type
            resolve_thresholds = [
                t.resolve_threshold for t in triggers if t.resolve_threshold is not None
            ]
            if resolve_thresholds:
                # Either grab the min or max resolve threshold depending on whether
                # we're an above or below threshold rule.
                func = min if threshold_type == 0 else max
                resolve_threshold = func(resolve_thresholds)
            else:
                resolve_threshold = None

            alert_rule.resolve_threshold = resolve_threshold
            alert_rule.threshold_type = threshold_type
        else:
            # Just a failsafe in case we have any bad rules without triggers.
            alert_rule.threshold_type = 0
        alert_rule.save()


class Migration(migrations.Migration):
    # This flag is used to mark that a migration shouldn't be automatically run in
    # production. We set this to True for operations that we think are risky and want
    # someone from ops to run manually and monitor.
    # General advice is that if in doubt, mark your migration as `is_dangerous`.
    # Some things you should always mark as dangerous:
    # - Large data migrations. Typically we want these to be run manually by ops so that
    #   they can be monitored. Since data migrations will now hold a transaction open
    #   this is even more important.
    # - Adding columns to highly active tables, even ones that are NULL.
    is_dangerous = False

    # This flag is used to decide whether to run this migration in a transaction or not.
    # By default we prefer to run in a transaction, but for migrations where you want
    # to `CREATE INDEX CONCURRENTLY` this needs to be set to False. Typically you'll
    # want to create an index concurrently when adding one to an existing table.
    atomic = False

    dependencies = [("sentry", "0088_rule_level_resolve_threshold_type")]

    operations = [
        migrations.RunPython(backfill_rule_level_fields, reverse_code=migrations.RunPython.noop)
    ]