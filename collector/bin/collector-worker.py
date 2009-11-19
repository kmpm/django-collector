#!/usr/bin/env python
from collector.worker import Worker
from collector.helpers.options import parse_args
            
if __name__ == "__main__":
    (options, args) = parse_args()
    try:
        worker = Worker(hostname=options.hostname, 
                port=options.port,
                userid=options.userid,
                password=options.password)
        worker.run()
    except Worker.WorkerException as ex1:
        print ex1
    except KeyboardInterrupt:
        print ""
        print "...closed"
        pass
    else:
        raise
    