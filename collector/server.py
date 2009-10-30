#!/usr/bin/env python

from carrot.messaging import Consumer
from carrot.messaging import Publisher
from carrot.connection import BrokerConnection
from datetime import datetime
import sys

class Server(object):
    def __init__(self, hostname='localhost', port=5672, **options):
        conn=BrokerConnection(hostname=hostname, port=port,
                    userid='collectoruser', password='password',
                    virtual_host='collectorvhost')
        
        self.publisher = Publisher(connection=conn, exchange="collector.response",
            exchange_type='direct',
            routing_key="response", serializer="json")
            
        self.consumer = Consumer(connection=conn, queue="feed",
                    exchange_type='topic',
                    exchange="collector", routing_key="collector.*.*")
                     
    
   
    def run(self):
        self.consumer.register_callback(self._get_request_callback)
        print "Waiting..."
        self.consumer.wait()
        
    def _get_request_callback(self, message_data, message):
        #print "message_data=%s" % message_data
        drivers=[]
        drivers.append(message_data)
        for obj in drivers:
            driver = None
            module_name = obj["driver_routing_key"]
            try:
                __import__(module_name)
                module = sys.modules[module_name]
                driver = module.Driver()
            except:
                raise
            values = []
            for tag in obj['tags']:
                if driver:
                    value = driver.read_value(tag['device'], tag['address'])
                else:
                    value="BAD_DRIVER"
                values.append({'name':tag['name'],
                        'current_value':value, 
                        'read_at':'2009-01-01'})
            self.publisher.send(values)
                        
        message.ack()
        
                
            
if __name__ == "__main__":
    server = Server()
    server.run()