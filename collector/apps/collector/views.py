# coding=utf-8
from django.db import models
from jsonrpc import jsonrpc_method
from models import *

@jsonrpc_method('collector.getTagList', safe=True)
def get_tag_list(request):
    tag_list = Tag.objects.all()
    list = []
    for tag in tag_list:
        list.append({'tag':tag.name, 'cv':tag.cv})
    return list

@jsonrpc_method('collector.getTag')
def get_tag(request, tag_name):
    tag=Tag.objects.get(name=tag_name)
    return {'tag':tag.name, 'cv':tag.cv}


@jsonrpc_method('collector.sayHello', safe=True)
def whats_the_time(request, name='Lester'):
    return "Hello %s" % name
  
@jsonrpc_method('collector.gimmeThat', authenticated=True)
def something_special(request, secret_data):
    return {'sauce': ['authenticated', 'sauce']}


