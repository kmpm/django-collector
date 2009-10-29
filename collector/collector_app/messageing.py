# coding=utf-8
from carrot.connection import DjangoBrokerConnection
from carrot.messaging import Publisher, Consumer
from models import Tag
import logging

def send_requests(requests, **options):
    logger = logging
    if 'logger' in options.keys():
        logger = options['logger']
        
    """Send a import request message to be picked up by workers."""
    connection = DjangoBrokerConnection()
    publisher = Publisher(connection=connection,
                              exchange="collector",
                              exchange_type='topic',
                              routing_key="collector.driver",
                              serializer='json')
    for req in requests:
        routing_key=req['driver_routing_key']        
        publisher.send(req, routing_key=routing_key)
        logger.debug("Sent request with routing_key %s:%s" %( routing_key,req,  ))
    publisher.close()
    connection.close()


def get_responses():
    connection = DjangoBrokerConnection()
    consumer = Consumer(connection=connection,
                              exchange="collector",
                              queue="responses",
                              routing_key="response.*")
    
    for message in consumer.iterqueue():
        responses = message.payload
        for resp in responses:
            tag=Tag.objects.get(name=resp['name'])
            print "Could have save %s for tag %s" % (resp['value'], tag.id,)
        message.ack()
        
    consumer.close()
    connection.close()
