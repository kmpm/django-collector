from optparse import OptionParser


def parse_args(parser=None):
    if not parser: parser=get_parser()
    #TODO:do something if config is used
    
    (options, args) = parser.parse_args()
    if options.config:
        raise Exception("config is not a implemented option")
    return (options, args)
    
def get_parser():
    parser = OptionParser()
    parser.add_option("-H", "--hostname", dest="hostname", default="localhost")
    parser.add_option("-p", "--port", dest="port", type='int', default="5672")
    parser.add_option("-u", "--userid", dest="userid", default="collectoruser")
    parser.add_option("-P", "--password", dest="password", default="password")
    parser.add_option("-v", "--vhost", dest="vhost", default="collectorvhost")
    parser.add_option("-c", "--config", dest="config", metavar="FILENAME")
    return parser