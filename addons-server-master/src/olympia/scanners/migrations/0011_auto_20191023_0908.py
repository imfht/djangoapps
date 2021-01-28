# Generated by Django 2.2.6 on 2019-10-23 09:08

from django.db import migrations

from olympia.constants.scanners import YARA


def update_matched_rules(apps, schema_editor):
    ScannerResult = apps.get_model('scanners', 'ScannerResult')
    ScannerRule = apps.get_model('scanners', 'ScannerRule')

    # `ScannerResult` is not our model, it is a different model auto-generated
    # for the migration, so we have to mimic the behavior of the `save()`
    # method.
    for result in ScannerResult.objects.filter(scanner=YARA, has_matches=True):
        rule_names = sorted({res['rule'] for res in result.results})
        matched_rules = ScannerRule.objects.filter(
            scanner=result.scanner, name__in=rule_names
        )
        result.has_matches = bool(matched_rules)
        result.save()
        for scanner_rule in matched_rules:
            result.matched_rules.add(scanner_rule)

    # In case a previous migration did set `has_matches=True` to non-Yara
    # results, let's change them because we cannot have matches for the other
    # scanners.
    ScannerResult.objects.exclude(scanner=YARA).update(has_matches=False)


class Migration(migrations.Migration):

    dependencies = [('scanners', '0010_auto_20191023_0908')]

    operations = [migrations.RunPython(update_matched_rules)]