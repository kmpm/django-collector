#!/usr/bin/env python

import sys, time
from collector.helpers.daemon import Daemon
from collector.worker import Worker
from collector.helpers.options import get_parser, parse_args
class Collectord(Daemon):
    def run(self):
        worker = Worker()
        worker.run()
        

if __name__ == "__main__":
    parser = get_parser()
    parser.add_option("--pid", default="/var/run/collectord.pid", dest="pidfile", metavar="PIDFILE")
    (options, args) = parse_args(parser)
    
    daemon = Collectord(options.pidfile)
    if len(args) == 1:
        if 'start' == args[0]:
            daemon.start()
        elif 'stop' == args[0]:
            daemon.stop()
        elif 'restart' == args[0]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
