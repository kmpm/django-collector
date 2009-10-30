#!/usr/bin/env python
# coding=utf-8
#Copyright (c) 2009 Peter Magnusson.
import unittest
import binascii
import logging 
import logging.config
from collector.drivers.sim import Driver as SimDriver

class TestSim(unittest.TestCase):
    
    def test_cache(self):
        from collector.helpers import cache
        rc = cache.set('test_key', 'test_value')
        self.assertNotEqual(0, rc)
        
        value = cache.get('test_key', 'default_value')
        self.assertEqual('test_value', value)
        
    def test_sim_driver(self):
        
        sd = SimDriver()
                
        value = sd.read_value('localhost', 'MW10')
        self.assertEqual("265", value)
        sd.write_value('localhost', 'MW10', "APA")
        value = sd.read_value('localhost', 'MW10')
        self.assertEqual("APA", value)

    def test_sim_randing(self):
        sd = SimDriver()
        value = sd.read_value('randint', '50, 55')
        self.assertTrue(value >=50)
        self.assertTrue(value <= 55)
        
        value = sd.write_value('randint', '50, 55', 10)
        self.assertTrue(value >=50)
        self.assertTrue(value <= 55)

if __name__ == '__main__':
	unittest.main()