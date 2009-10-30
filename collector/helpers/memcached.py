#!/usr/bin/env python
try:
    import cmemcache as memcache
except ImportError:
    import memcache
    
class CacheClass(object):
    def __init__(self):
        self.client = memcache.Client(['127.0.0.1:11211'], debug=0)

    def get(self, key, default=None):
        cache_value = self.client.get(fixkey(key))
        if cache_value: return cache_value
        return default

    def set(self, key, value, time=0):
        return self.client.set(fixkey(key), value, time)

def fixkey(key):
    return key.replace(" ", "_")