from django.db import models


class SearchableModel1(models.Model):
    name = models.CharField(max_length=128)
    other_thing = models.CharField(max_length=128, default="1")


class SearchableModel2(models.Model):
    sid = models.CharField(primary_key=True, max_length=10)
