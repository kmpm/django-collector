# coding=utf-8
from django.test import TestCase
from models import *
from datetime import datetime


#from jsonrpc.proxy import ServiceProxy
from django.test import Client
from django.core.urlresolvers import reverse


#class TestTag(TestCase):
#    fixtures = ['testdata.json']
    
#    def test_tags_on_driver(self):
#        driver = Driver.objects.get(id=1)
#        tags = driver.tags.all()
#        self.assertEqual(1, len(tags))

#    def test_driver_on_tag(self):
#        tag = Tag.objects.get(id=1)
#        self.assertEqual('Sim', tag.driver.slug)
                
#    def test_driver_on_tag_through_slug(self):
#        tags = Tag.objects.filter(driver__slug='Sim')
#        self.assertEqual(1, len(tags))

#    def test_tags_to_be_polled(self):
#        tags = Tag.objects.filter(driver__poll_next_at__lte=datetime.now())
#        self.assertEqual(1, len(tags))

#    def test_tag_read(self):
#        tag = Tag.objects.all()[:1][0]
#        value = tag.read_value()
#        tag.save()
 
class TestMessageing(TestCase):
    def test_amqp(self):
        from carrot.connection import DjangoBrokerConnection
        from carrot.messaging import Publisher, Consumer
        
        connection = DjangoBrokerConnection()
        publisher = Publisher(connection=connection,
                              exchange="collector",
                              exchange_type='topic',
                              routing_key="collector.driver",
                              serializer='json')
        publisher.send("test")
        publisher.close()
        connection.close()
        
    def test_send_req(self):
        from messageing import send_requests
        send_requests([{'driver_routing_key': 'collector.driver.test', 
            'data':"test_send_req"}])
   
#class TestJson(TestCase):
#    URL='http://localhost:8000/collector/json/'
#    def test_tag_list(self):
#        s = ServiceProxy(self.URL)
        
        
#        result = s.collector.getTagList()
#        tags=result['result']
#        self.assertTrue(len(tags)>0)
#        self.assertEqual(result['error'], None)
#        self.assertEqual(tags[0]['tag'], 'SIM_TEMP_1')
#        #print repr(s.collector.getTagList())
#        #print repr(s.collector.getTag('SIM_TEMP_1'))

#    def test_json_html(self):
#        client=Client()
#        response = client.post('/collector/json/',{'method':'collector.getTagList', 'params':None, 'id':'jsonrpc'} )
#        self.assertEqual("", repr(response.content))
        