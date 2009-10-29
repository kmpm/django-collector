# coding=utf-8
from django.db import models
#from jsonrpc import jsonrpc_method
from models import *

#@jsonrpc_method('collector.getTagList')
#def get_tag_list(request):
#    tag_list = Tag.objects.all()
#    list = []
#    for tag in tag_list:
#        list.append({'tag':tag.slug, 'cv':tag.cv})
#    return list

#@jsonrpc_method('collector.getTag')
#def get_tag(request, tag_name):
#    tag=Tag.objects.get(slug=tag_name)
#    return {'tag':tag.slug, 'cv':tag.cv}


#@jsonrpc_method('collector.sayHello')
#def whats_the_time(request, name='Lester'):
#    return "Hello %s" % name
  
#@jsonrpc_method('collector.gimmeThat', authenticated=True)
#def something_special(request, secret_data):
#    return {'sauce': ['authenticated', 'sauce']}


