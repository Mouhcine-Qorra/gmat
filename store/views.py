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
        machine = ifa.machine
    except:
        machine = 'None'
    try:
        mc = gma()
    except:
        mc = '0.0.0.0'
    try:
        system = ifa.system
    except:
        system = 'None'
    ip = f'mc:{mc};;machine:{machine};;system:{system};;processor:{processor}'
    try:
        Customer.objects.get(ip=ip)
        print(f'\n\n found ip: {ip}')
    except:
        Customer.objects.create(name=mc, email=mc+'@gmail.com', ip=ip)
        print(f"\n\n didn't found ip: {ip}")
    return render(request, 'store/store.html', {})
