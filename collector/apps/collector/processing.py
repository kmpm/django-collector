# coding=utf-8
from datetime import datetime, timedelta
#from plant.collector.messageing import MessageBus
from models import *
from django.conf import settings
import logging
from messageing import *




#def trigger_update(**kwargs):
#    tags = Tag.objects.all()
#    for tag in tags:
#        send_update_request_trigger(tag.id)
#    
#    

def process_responses(logger=logging, **kwargs):
    get_responses(logger)
    
    
def poll_external(logger=logging):
    drivers=_drivers_to_poll(logger)
    requests=[]
    logger.info("%s drivers to poll" % len(drivers))
    for driver in drivers:
        request = {
            'request_at':str(datetime.now()),
            'driver_name':driver.name, 
            'driver_routing_key':driver.routing_key}
        tags = driver.tags.all()
        tag_list=[]
        logger.info("%s tags to poll for driver %s" % (len(tags), driver.name))
        for tag in tags:
            obj={'name':tag.name, 'device':tag.device, 
                'address':tag.address,
                'set_value':None}
            tag_list.append(obj)
        request['tags']=tag_list
        requests.append(request)
    send_requests(requests, logger=logger)
    

def poll_internal(logger=logging):
    tags = _tags_to_poll(logger)
    logger.info("Amount of tags=%s" %len(tags))
    drivers = []
    for tag in tags:
        value = tag.read_value()
        if value.cv == None:
            logger.info("Tag %s returned None" % tag.slug)
        if not tag.driver in drivers:
            drivers.append(tag.driver)
    for driver in drivers:
        logger.info('Processing driver %s' % driver.slug)
        driver.polled()
        driver.save()
        
def _drivers_to_poll(logger):
    drivers = Driver.objects.filter(poll_next_at__lte=datetime.now(), enabled=True)
    return drivers
    
def _tags_to_poll(logger):
    logger.info("Checking tags to poll")
    tags = Tag.objects.filter(driver__poll_next_at__lte=datetime.now(), driver__enabled=True, enabled=True).order_by('device', 'address')
    return tags
    
    
