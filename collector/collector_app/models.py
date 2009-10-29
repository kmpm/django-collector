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
    pv = models.CharField(_('previous value'), max_length=20, blank=True, null=True)
    sv = models.CharField(_('set value'), max_length=20, blank=True, null=True)
    last_read_at = models.DateTimeField(_('last read at'), default=datetime.now)
    last_write_at = models.DateTimeField(_('last write at'), default=datetime.now)
    last_change_at = models.DateTimeField(_('last change at'), default=datetime(1900, 01, 01, 00,00,01))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('driver', 'device', 'address')
    
    def __unicode__(self):
        return self.name
    
    def read_value(self):
        name = self.driver.driver_package
        __import__(name)
        module = sys.module[name]
        driver = module.Driver()
        value = driver.read_value(self.device, self.address)
        self.save_with_history(value)
        return value
    
    def save_with_history(self, value):
        if self.cv != value:
            self.logs.create(v=value)
            self.pv = self.cv
            self.last_change_at = datetime.now()
        self.cv = value
        self.last_read_at = datetime.now()
        self.save()

    
    
class TagLog(models.Model):
    tag = models.ForeignKey(Tag, verbose_name=_('tag'), related_name="logs")
    v = models.CharField(_('value'), max_length=20)
    created_at = models.DateTimeField(_('created at'), default=datetime.now)
    
    class Meta:
        ordering = ['-created_at']
    
    