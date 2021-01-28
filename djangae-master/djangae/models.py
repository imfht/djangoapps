from django.db import models

from djangae import patches  # noqa


class DeferIterationMarker(models.Model):
    """
        Marker to keep track of sharded defer
        iteration tasks
    """

    # Set to True when all shards have been deferred
    is_ready = models.BooleanField(default=False)

    shard_count = models.PositiveIntegerField(default=0)
    shards_complete = models.PositiveIntegerField(default=0)

    delete_on_completion = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    callback_name = models.CharField(max_length=100)
    finalize_name = models.CharField(max_length=100)

    class Meta:
        app_label = "djangae"

    @property
    def is_finished(self):
        return self.is_ready and self.shard_count == self.shards_complete

    def __unicode__(self):
        return "Background Task (%s -> %s) at %s" % (
            self.callback_name,
            self.finalize_name,
            self.created
        )
