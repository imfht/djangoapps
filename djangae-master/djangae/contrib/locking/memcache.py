import random
import time
from datetime import datetime

from django.core.cache import cache


class MemcacheLock(object):
    def __init__(self, identifier, cache, unique_value):
        self.identifier = identifier
        self._cache = cache
        self.unique_value = unique_value

    @classmethod
    def acquire(cls, identifier, wait=True, steal_after_ms=None):
        start_time = datetime.utcnow()
        unique_value = random.randint(1, 100000)

        while True:
            acquired = cache.add(identifier, unique_value)
            if acquired:
                return cls(identifier, cache, unique_value)
            elif not wait:
                return None
            else:
                # We are waiting for the lock
                if (datetime.utcnow() - start_time).total_seconds() * 1000 > steal_after_ms:
                    # Steal anyway
                    cache.set(identifier, unique_value)
                    return cls(identifier, cache, unique_value)

                time.sleep(0)

    def release(self):
        cache = self._cache

        # Delete the key if it was ours. There is a race condition here
        # if something steals the lock between the if and the delete...
        if cache.get(self.identifier) == self.unique_value:
            cache.delete(self.identifier)
