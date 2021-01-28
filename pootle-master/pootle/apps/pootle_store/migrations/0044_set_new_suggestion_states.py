# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 05:48
from __future__ import unicode_literals

from django.db import migrations


class OLDSuggestionStates(object):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'


def set_suggestion_states(apps, schema_editor):
    suggestions = apps.get_model("pootle_store.Suggestion").objects.all()
    states = apps.get_model("pootle_store.SuggestionState").objects.all()
    pending = states.get(name="pending")
    accepted = states.get(name="accepted")
    rejected = states.get(name="rejected")
    suggestions.filter(tmp_state=OLDSuggestionStates.PENDING).update(state_id=pending.id)
    suggestions.filter(tmp_state=OLDSuggestionStates.ACCEPTED).update(state_id=accepted.id)
    suggestions.filter(tmp_state=OLDSuggestionStates.REJECTED).update(state_id=rejected.id)


class Migration(migrations.Migration):

    dependencies = [
        ('pootle_store', '0043_suggestion_state'),
    ]

    operations = [
        migrations.RunPython(set_suggestion_states),
    ]