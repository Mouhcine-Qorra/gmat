from django.shortcuts import render, redirect
from .models import *
from getmac import get_mac_address as gma


def store(request):
    try:
        ip = gma()
    except Exception:
        ip = '0.0.0.0'
    try:
        customer = Customer.objects.get(ip=ip)
        print(f'\n\n found ip: {ip}')
    except:
        customer = Customer.objects.create(name=ip, email=ip+'@gmail.com', ip=ip)
        print(f"\n\n didn't found ip: {ip}")
    return render(request, 'store/store.html', {})
