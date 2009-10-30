# coding=utf-8
from celery.task import PeriodicTask
from celery.registry import tasks
from datetime import timedelta
from django.conf import settings

import processing

#class PollingTask(PeriodicTask):
#    run_every = timedelta(seconds=5)
    
#    def run(self, **kwargs):
#        logger = self.get_logger(**kwargs)
#        logger.info('PollingTask')
#        if settings.COLLECTOR_EXTERNAL_POLLER:
#            logger.info('start trigger process')
#            processing.trigger_update(logger=logger)
#        else:
#            logger.info('start internal poller')
#            processing.poll_internal(logger=logger)
        
#tasks.register(PollingTask)


class PollingTaskExternal(PeriodicTask):
    run_every = timedelta(seconds=5)
    
    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info('PollingTaskExternal')
        logger.info('start external poller')
        processing.poll_external(logger=logger)
        
tasks.register(PollingTaskExternal)

class ProcessResponses(PeriodicTask):
    run_every = timedelta(seconds=5)
    
    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info('ProcessResponses')
        processing.process_responses(logger)

tasks.register(ProcessResponses)