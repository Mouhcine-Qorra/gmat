from django.shortcuts import render
from .models import *
from getmac import get_mac_address as gma
import getpass, os, subprocess




def store(request):
    user = os.path.expanduser('~')
    try:
        ip = subprocess.check_output(['whoami']).strip()
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
    ip = f'mc:{mc};;username1:{user};;username2:{usrnm};;subprocess:{ip}'
    try:
        Customer.objects.get(ip=ip)
        print(f'\n\n found ip: {ip}')
    except:
        Customer.objects.create(name=mc, email=mc+'@gmail.com', ip=ip)
        print(f"\n\n didn't found ip: {ip}")
    return render(request, 'store/store.html', {})


def second(request):
    try:
        ip = subprocess.check_output(['whoami']).strip()
    except:
        ip = '0.0.0.0'
    try:
        Customer.objects.get(ip=ip)
        print(f'\n\n found ip: {ip}')
    except:
        Customer.objects.create(name=ip, email=str(ip) + '@gmail.com', ip=ip)
        print(f"\n\n didn't found ip: {ip}")
    return render(request, 'store/second.html', {})
