
# Northstar AI - Authorization Cache Prototype

import time


class PermissionCache:
    def __init__(self, role_provider, ttl_seconds=300,
                 clock=time.monotonic):
        self.role_provider = role_provider
        self.ttl_seconds = ttl_seconds
        self.clock = clock
        self.cache = {}

    def get_role(self, username):
        now = self.clock()
        entry = self.cache.get(username)

        # Only reuse an unexpired permission entry.
        if entry and now < entry["expires_at"]:
            return entry["role"]

        # Expired permissions must be revalidated.
        # If the trusted source fails, deny access.
        try:
            role = self.role_provider(username)
        except Exception:
            self.cache.pop(username, None)
            return None

        if role is None:
            self.cache.pop(username, None)
            return None

        self.cache[username] = {
            "role": role,
            "expires_at": self.clock() + self.ttl_seconds
        }
        return role

    def invalidate(self, username):
        self.cache.pop(username, None)
