from django.conf.urls.defaults import *
from django.conf import settings

from jsonrpc import jsonrpc_site

import views # you must import the views that need connected


urlpatterns = patterns('',
    url(r'^json/browse/', 'jsonrpc.views.browse', name="jsonrpc_browser"), # for the graphical browser/web console only, omissible
    (r'^json/(?P<method>[a-zA-Z0-9.]+)$', jsonrpc_site.dispatch), # for HTTP GET only, also omissible    
    url(r'^json/', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
    

)



