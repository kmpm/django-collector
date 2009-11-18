# coding=utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, timedelta
import sys

class Driver(models.Model):
    POLL_STATUS_CHOICES = (
        ('AA', _('Ready')),
        ('BA', _('Running')),
        ('CA', _('Finished')),
        ('ZA', _('Finished with errors')),
    )
    name = models.SlugField(verbose_name=_('name'))
    routing_key = models.CharField(_('driver routing key'), max_length=150)
    enabled = models.BooleanField(_('enabled'), default=True)
    poll_interval = models.IntegerField(_('poll interval'), default=10)
    polled_at = models.DateTimeField(_('polled at'), default=datetime.now)
    poll_next_at = models.DateTimeField(_('poll next at'), default=datetime.now)
    poll_status = models.CharField(_('poll status'), max_length=2, default='AA', choices=POLL_STATUS_CHOICES)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    def __unicode__(self):
        return self.name
    
    def polled(self):
        self.poll_next_at = datetime.now() + timedelta(seconds=self.poll_interval)


class Tag(models.Model):
    name = models.SlugField(verbose_name=_('name'), unique=True)
    driver = models.ForeignKey(Driver, related_name='tags', verbose_name=_('driver'))
    device= models.CharField(_('device'), max_length=100)
    address = models.CharField(_('address'), max_length=100)
    enabled = models.BooleanField(_('enabled'), default=True)
    comment = models.CharField(_('comment'), max_length=200, blank=True)
    cv = models.CharField(_('current value'), max_length=20, blank=True, null=True)
    data_good=models.BooleanField(_('data good'), default=True)
    pv = models.CharField(_('previous value'), max_length=20, blank=True, null=True)
    formula = models.CharField(_('formula'), max_length=200, blank=True, null=True)
    alarm_rule = models.CharField(_('alarm rule'), max_length=200, blank=True, null=True)
    alarm=models.BooleanField(_('alarm'), default=False)
    raw_value= models.CharField(_('raw value'), max_length=20, blank=True, null=True)
    last_change_at = models.DateTimeField(_('last change at'), default=datetime(1900, 01, 01, 00,00,01))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('driver', 'device', 'address')
    
    def __unicode__(self):
        return self.name
    
    
    def save_with_history(self, value):
        if self.raw_value != value:
            self.good_data=True
            #calculate cv
            if self.formula:
                try:
                    self.cv = eval(self.formula)
                except:
                    self.cv="BAD_DATA"
                    self.good_data=False
            else:
                self.cv = value
            
            #check if alarm
            if self.alarm_rule:
                try:
                    if eval(self.alarm_rule):
                        self.alarm=True
                    else:
                        self.alarm=False
                except:
                    self.alarm=True
            self.raw_value=value
            self.last_change_at = datetime.now()
            #save the new value
            self.pv = self.cv
            self.save()
            #create a log
            self.logs.create(v=self.cv, raw_value=value, alarm=self.alarm)
            

    
    
class TagLog(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('tag'), related_name="logs")
    v = models.CharField(_('value'), max_length=20, blank=True, null=True) 
    raw_value = models.CharField(_('raw value'), max_length=20, blank=True, null=True) 
    alarm=models.BooleanField(_('alarm'), default=False)
    created_at = models.DateTimeField(_('created at'), default=datetime.now)
    
    class Meta:
        ordering = ['-created_at']
    
    