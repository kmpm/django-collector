# coding=utf-8
from django.core.cache import cache
from collector.drivers.base import Driver as BaseDriver
from socket import *
import logging

def setBit( x, bitNum ):
  return x | 1 << bitNum
def clearBit( x, bitNum ):
  return x & ~( 1 << bitNum )
def checkBit( x, bitNum ):
  return (x & (1<<bitNum)) != 0

class AddressException(Exception):
    pass

class FstAddress(str):
    VALID_DATATYPES=['M', 'E']
    def __init__(self, content):
        content = content.upper()
        
        if "." in content and "W" in content:
            raise AddressException("Bad format of address %s. Words can not access bits" % content)

        self.bit = None
        self.datatype=""
        self.word=""
        for s in content[0:2]:
            if s.isalpha():
                self.datatype = self.datatype + s
        datatype_length=len(self.datatype)
        if datatype_length==1 and not ("." in content):
            raise AddressException("Bad format of address %s. Bit part of address is missing" % content)
        self.datatype=self.datatype[0:1] #always first char. second is if it's a word
        
        if "." in content:
            dotPos = content.find(".")
            self.bit = int(content[dotPos+1:])
        if self.bit != None:
            self.word = int(content[datatype_length:content.find(".")])
        else:
            self.word = int(content[datatype_length:])
            
        
        
        
    
    def __str__(self):
        if self.bit:
            return self.bit_addr()
        else:
            return self.word_addr
    
    @property
    def word_addr(self):
        return "%sW%s" % (self.datatype, self.word)
        
    def bit_addr(self, bit=None):
        if not bit:
            bit=self.bit
        return "%s%s.%s" % (self.datatype, self.word, self.bit)


class Driver(BaseDriver):
    """
    Driver for communicating with Festo PLCs using the CI protocol.
    
    ::Inputs::
    device = IP or hostname of the PLC
    address = Address of value to display or change. E0.1 equals Input block 0 bit 1
    
    ::Outputs::
    Returns a instance of DriverValue
    """
    CACHE_TIMEOUT=1
    PORT_CI=992
    
    
    def read_value(self, device, address):
        adr = FstAddress(address) #checks the format of the address
        if self.CACHE_TIMEOUT==0:
            real_value = self._read(device, address)
        else:
            cache_value=None
            cache_value = cache.get(self._key(device,adr.word_addr), None)
    
            if cache_value:
                #if we have a cached value use that one...
                real_value=cache_value
            else:
                #else get a new proper one
                real_value = self._read(device, adr.word_addr)
                self._cache(device, adr.word_addr, real_value)
            
            #
            if (adr.bit != None) and (real_value != None):
                if checkBit(int(real_value), adr.bit):
                    real_value='1'
                else:
                    real_value='0'
                    
        value = DriverValue(real_value)
        return value
    
    def write_value(self, device, address, set_value):
        value = self.read_value(device, address)
        value.sv=set_value
        #TODO: write to festo CI
        return value
    
            
    def _cache(self, device, address, new_value):
        cache.set(self._key(device, address), new_value, self.CACHE_TIMEOUT)
        
    
    def _read(self, device, address):
        s = socket(AF_INET, SOCK_DGRAM)
        cmd = "D%s" % address #D for display
        s.sendto(cmd, (device, self.PORT_CI))
        s.settimeout(1)
        try:
            reply, server = s.recvfrom(255)
            if cmd in reply:
                #a interpretable value, check next
                if "ERROR" in reply:
                    return None
                values = reply.split("=")
                return values[1]
            else:
                return None
        except:
            return None
        
    
    def _key(self, device, address):
        return "fstci_%s_%s" % (device, address)
