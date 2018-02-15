# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import JunosDevice
from mplsbgp.mplscommands import get_mpls_info
from mplsbgp.bgpcommands import get_bgp_routes

# Choose between MPLS and BGP information
def index(request):
    return render(request, 'mplsbgp/index.html')

# Enter MPLS query
def mpls(request):
    device_list = JunosDevice.objects.all()
    context = { 'device_list' : device_list } 
    return render(request, 'mplsbgp/mpls.html', context)

# Enter BGP query
def bgp(request):
    device_list = JunosDevice.objects.all()
    context = { 'device_list' : device_list }
    return render(request, 'mplsbgp/bgp.html', context)

# defs mpls/bgp result could have used a same template and pass the correspondent
# variables from their view. But for future enhancing of the view they are separate.
# Present MPLS results according to the query
def mplsresult(request):
    hostn = request.POST['hostname']
    regex = request.POST['regex']
    device = JunosDevice.objects.get(hostname=hostn)
    output = get_mpls_info(device.ip, device.user, device.password, regex, device.logical_system)
    context = { 'hostname' : hostn,
                'regex' : regex ,
                'output' : output
                }
    return render(request, 'mplsbgp/mplsresult.html', context)

# Present BGP results according to the query
def bgpresult(request):
    hostn = request.POST['hostname']
    regex = request.POST['regex']
    device = JunosDevice.objects.get(hostname=hostn)
    output = get_bgp_routes(device.ip, device.user, device.password, regex, device.logical_system)
    context = { 'hostname' : hostn,
                'regex' : regex ,
                'output' : output
                }
    return render(request, 'mplsbgp/bgpresult.html', context)
