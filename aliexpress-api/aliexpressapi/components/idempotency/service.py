class IdempotencyService:
    def __init__(self, cache):
        self.cache = cache

    def acquire(self, key: str) -> bool:
        return self.cache.add(key, "LOCKED", ttl=3600)


class IdempotencyService:
    def __init__(self, cache):
        self.cache = cache

    def acquire(self, key: str) -> bool:
        if not key:
            return False
        return self.cache.add(
            key=f"idempotency:{key}",
            value="LOCKED",
            ttl=3600,
        )
