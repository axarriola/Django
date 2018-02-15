# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

#Represents one Junos physical device or one logical system
class JunosDevice(models.Model):
    ip = models.CharField(max_length=200)
    hostname = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    logical_system = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.hostname
