# coding=utf-8
#from django.core.cache import cache
from collector.drivers.base import Driver as BaseDriver
from collector.helpers import cache
import random

class Driver(BaseDriver):
    
    def __init__(self):
        self.write_value('localhost', 'MW10', '265')
        self.write_value('localhost', 'MW11', '200')
    
    def read_value(self, device, address):
        if device=='randint':
            a, b = address.split(",")
            result = random.randint(int(a), int(b))
        else:
            result = cache.get(self._key(device, address), None)
        return result
        
    def write_value(self, device, address, set_value):
        cache.set(self._key(device, address), set_value, 10*60)
        value = self.read_value(device, address)
        return value
    
    def _key(self, device, address):
        return "%s:%s" % (device, address, )