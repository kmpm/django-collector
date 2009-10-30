from django.conf.urls.defaults import *
from django.conf import settings

#from jsonrpc import jsonrpc_site

import collector.apps.tagheap.views # you must import the views that need connected

urlpatterns = patterns('', 
    #(r'^json/', jsonrpc_site.dispatch)
)



