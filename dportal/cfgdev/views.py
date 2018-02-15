# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from mplsbgp.models import JunosDevice
from cfgdev.cfgcommands import input_conf, cfgcommit, cfgrollback

# Choose which device to configure
def index(request):
    device_list = JunosDevice.objects.all()
    context = { 'device_list' : device_list }
    return render(request,'cfgdev/index.html',context)

# Input VRF configuration information
def cfginput(request):
    hostn = request.POST['hostname']
    return render(request,'cfgdev/cfginput.html', { 'hostname' : hostn })

# Preview the "show | compare" and decide to commit or rollback
def cfgpreview(request):
    hostn = request.POST['hostname']
    dev = JunosDevice.objects.get(hostname=hostn)
    preview = input_conf(dev.ip,dev.user,dev.password,request.POST)
    return render(request, 'cfgdev/cfgpreview.html', {'preview':preview, 'hostname': hostn})

def commit(request):
    cfgcommit()
    return render(request, 'cfgdev/commit.html')

def rollback(request):
    cfgrollback()
    return render(request, 'cfgdev/rollback.html')
