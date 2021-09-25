from .models import Order, Customer
from ipware import get_client_ip


def minfunc(request):
    total, total_items = 0, 0
    if request.user.is_authenticated:
        customer = request.user.customer
        try:
            order, created = Order.objects.get_or_create(customer=customer)
        except:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.filter(to_order=False)
        for item in items:
            total = total + float(item.quantity_price())
        for item in items:
            total_items = total_items + item.quantity
    else:
        ip, is_routable = get_client_ip(request)
        if not ip:
            ip = '0.0.0.0'
        IP = f"{ip}||{str(request.META['HTTP_USER_AGENT'])}"
        try:
            customer = Customer.objects.get(ip=IP)
        except:
            customer = Customer.objects.create(name=IP, email=IP+'@gmail.com', ip=IP)
        try:
            order, created = Order.objects.get_or_create(customer=customer)
        except:
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.filter(to_order=False)
        for item in items:
            total = total + float(item.quantity_price())
        for item in items:
            total_items = total_items + item.quantity
    return {'total_items': total_items, 'total': total, 'items': items, 'order': order}
