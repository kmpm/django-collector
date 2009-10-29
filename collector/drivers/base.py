# coding=utf-8

def abstract():
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + ' must be implemented in subclass')

class Driver(object):    
    def read_value(self, device, address): abstract()
    def write_value(self,device, address, set_value): abstract()