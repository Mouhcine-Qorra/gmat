from django.shortcuts import render, redirect
from .models import *
from getmac import get_mac_address as gma
import platform, re, uuid



def store(request):
    ifa = platform.uname()
    try:
        processor = ifa.processor
    except:
        processor = 'None'
    try:
        mc = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    except:
        mc = 'None'
    ip = f'mc:{mc};;processor:{processor}'
    print(f'\n\n processor: {processor}, \nsystem: {ifa.system}, \nnode: {ifa.node}, \nmachine: {ifa.machine}, \nmc: {mc}')
    try:
        Customer.objects.get(ip=ip)
        print(f'\n\n found ip: {ip}')
    except:
        Customer.objects.create(name=mc, email=mc+'@gmail.com', ip=ip)
        print(f"\n\n didn't found ip: {ip}")
    return render(request, 'store/store.html', {})
