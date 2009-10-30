# coding=utf-8

def get_cache():
    import memcached as module
    return getattr(module, 'CacheClass')()
    
cache = get_cache()
    