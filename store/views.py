from django.shortcuts import render, redirect
from .models import *
from getmac import get_mac_address as gma
import getpass, os
from ipware import get_client_ip as getip


def store(request):
    user = os.path.expanduser('~')
    try:
        ip = getip()
    except:
        ip = '0.0.0.0'
    try:
        mc = gma()
    except:
        mc = '0.0.0.0'
    try:
        usrnm = (getpass.getuser())
    except:
        usrnm = 'None'
    ip = f'mc:{mc};;username:{user};;ip:{ip}'
    try:
        Customer.objects.get(ip=ip)
        print(f'\n\n found ip: {ip}')
    except:
        Customer.objects.create(name=mc, email=mc+'@gmail.com', ip=ip)
        print(f"\n\n didn't found ip: {ip}")
    return render(request, 'store/store.html', {})
