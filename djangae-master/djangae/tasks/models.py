from django.db import models


class DeferredTask(models.Model):
    data = models.BinaryField()
